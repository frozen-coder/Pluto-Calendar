const calendar = document.querySelector(".calendar"),
  date = document.querySelector(".date"),
  daysContainer = document.querySelector(".days"),
  prev = document.querySelector(".prev"),
  next = document.querySelector(".next"),
  todayBtn = document.querySelector(".today-btn"),
  gotoBtn = document.querySelector(".goto-btn"),
  dateInput = document.querySelector(".date-input");
  eventday = document.querySelector(".event-day"),
  eventDate = document.querySelector(".event-date"),
  eventsContainer = document.querySelector(".events "),
  addEventSubmit = document.querySelector(".add-event-btn ");
let today = new Date();
let activeDay;
let month = today.getMonth();
let year = today.getFullYear();

const months = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December",
];

//set a empty array
let eventsArr = [];

getEvents();
// Function to add days
function toYearMonthDayFormat(dateObject){
  //alert(dateObject.getFullYear() + "-" + (dateObject.getMonth()+1) + "-0"+dateObject.getDay());
  
  if(dateObject.getDay() < 10) {
    return dateObject.getFullYear() + "-" + (dateObject.getMonth()+1) + "-0"+dateObject.getDate();
  }
  return dateObject.getFullYear() + "-"+(dateObject.getMonth()+1)+"-"+dateObject.getDate();
}
function addEvent(eventObject) {
  //alert(eventObject);
  const timeFrom = converTime(eventObject.eventTimeFrom);
  const timeTo = converTime(eventObject.eventTimeTo);
  const eventTitle = eventObject.title;
  let eventDate = eventObject.date;
  let eventDateArray = eventDate.split("-");
  let eventDay = eventDateArray[2];
  let eventMonth = eventDateArray[1];
  let eventYear = eventDateArray[0];
  const newEvent = {
    title: eventTitle,
    time : timeFrom + " - " + timeTo,
  };
  let eventAdded = false;
  if(eventsArr.length > 0) {
    // cehck if current day hasalready any event then add to that
    eventsArr.forEach((item) =>  {
      if(
        item.day == eventDay &&
        item.month == eventMonth &&
        item.year == eventYear
      ) {
        item.events.push(newEvent);
        eventAdded = true;
      }
    })
  }

  //if event array empty or current day has not event create new
  if(!eventAdded) {
    eventsArr.push ({
      day: eventDay,
      month: eventMonth,
      year: eventYear,
      events: [newEvent],
    });
  }
  updateEvents(eventDay);

  // also add event class to newly added day if not already 
  //TODO: Fix the weird bug where events on the current day appear when they shoulden't
  const activeDayElem = document.querySelector(".day.active");
  if(!activeDayElem.classList.contains("event")) {
    activeDayElem.classList.add("event")
  }
  

}
function initCalendar() {
  // to get prev month days an current month all days and rem next month days
  const firstDay = new Date(year, month, 1);
  const lastDay = new Date(year, month + 1, 0);
  //console.log(month);
  //console.log(month+1);
  const prevLastDay = new Date(year, month, 0);
  const prevDays = prevLastDay.getDate();
  const lastDate = lastDay.getDate();
  const day = firstDay.getDay();
  const nextDays = 7 - lastDay.getDay() - 1;
  var url = "http://"+window.location.hostname+":"+location.port+"/plutocalendar/get_tasks_date_range";
  //alert("Yo, the url u are trying to use for initCalendar is " + url);
  let formData = new FormData();
  formData.append('startDate', toYearMonthDayFormat(firstDay));
  
  formData.append('endDate', toYearMonthDayFormat(lastDay));
  responseDate = "";
  //console.log(firstDay.);
  //console.log(lastDay);
  fetch(url,
   {   method: 'POST',  
   
      body: formData, 
      }
    )  
     .then(function(res){return res.json();})
     .then(function(data){
      //alert(JSON.stringify(data));
      dataProccessed = JSON.parse(JSON.stringify(data));
      //alert("Data proccessed = " + dataProccessed);
      //alert("First obj = " + dataProccessed[0]);
      for(let i = 0; i < dataProccessed.length; i++) {
        //alert("Event added");
        //alert("Object is " + dataProccessed[i]);
        addEvent( dataProccessed[i]);
      }
    })   
     .catch(error => console.error('Error posting data:', error));
  //Update date on the top of the callendar
  date.innerHTML = months[month] + " " + year;

  //Adding days on dom
  let days = "";

  //prev months
  for (let x = day; x > 0; x--) {
    days += `<div class="day prev-date">${prevDays - x + 1}</div>`;
  }

  // cuurent month days

  for (let i = 1; i <= lastDate; i++) {

    // check if event present on current day
    let event = false;
    eventsArr.forEach((eventObj) => {
      if (
        eventObj.day == i &&
        eventObj.month == month+1 &&
        eventObj.year == year
      ) {
        // if event found
        event = true;
      }
    })

    //if day is today add class today
    if (
      i == new Date().getDate() &&
      year == new Date().getFullYear() &&
      month == new Date().getMonth()
    ) {

      activeDay = i;
      getActiveDay(i);
      updateEvents(i);
      //if event foutn also add event class
      // add active on today at startup
      if (event) {
        days += `<div class="day today active event">${i}</div>`;
      } else {
        days += `<div class="day today active">${i}</div>`;
      }
    } else {
      if (event) {
        days += `<div class="day event">${i}</div>`;
      } else {
        days += `<div class="day ">${i}</div>`;
      }
    }
  }

  // next month days
  for(let j = 1; j<nextDays; j++) {
    days += `<div class="day next-date">${j} </div>`;
  }


  daysContainer.innerHTML = days;
  // add listner after callendar initialized
  addListner();
}
initCalendar();


// prev month

function prevMonth() {
  month--;
  if(month<0) {
    month = 11;
    year--;
  }

  initCalendar();
}

//next month

function nextMonth() {
  month++;
  if(month>11) {
    month = 0;
    year++;
  }
  initCalendar();
}

// add event listener on prev and next

prev.addEventListener("click", prevMonth)
next.addEventListener("click",nextMonth)


// our calendar is ready
// lets add goto date and goto today functionality


todayBtn.addEventListener("click", () => {
  today = new Date();
  month = today.getMonth();
  year = today.getFullYear();
  initCalendar();
})

dateInput.addEventListener("input", (e) => {
  // allow only numbers remove anyting else
  dateInput.value = dateInput.value.replace(/[^0-9/]/g, "");
  if(dateInput.value.length == 2) {
    //add a slash if two numbers entered
    dateInput.value += "/";
  }
  if(dateInput.value.length > 7) {
    // dont allow more than 7 characters
    dateInput.value = dateInput.value.slice(0,7);
  }

  // if backspace pressed
  if (e.inputType === "deleteContentBackward") {
    if (dateInput.value.length === 3) {
      dateInput.value = dateInput.value.slice(0, 2);
    }
  }
});


gotoBtn.addEventListener("click", gotoDate);

// function to go to entered date
function gotoDate() {
  console.log("here");
  const dateArr = dateInput.value.split("/");
  // data validation
  if (dateArr.length === 2) {
    if (dateArr[0] > 0 && dateArr[0] < 13 && dateArr[1].length === 4) {
      month = dateArr[0] - 1;
      year = dateArr[1];
      initCalendar();
      return;
    }
  }
  alert("Invalid Date");
}

const addEventBtn = document.querySelector(".add-event"),
 addEventContainer = document.querySelector(".add-event-wrapper"),
 addEventCloseBtn = document.querySelector(".close"),
 addEventTitle = document.querySelector(".event-name"),
 addEventFrom = document.querySelector(".event-time-from"),
 addEventTo = document.querySelector(".event-time-to")


 
addEventBtn.addEventListener("click", () => {
  addEventContainer.classList.toggle("active");
});

addEventCloseBtn.addEventListener("click", () => {
  addEventContainer.classList.remove("active");
});

document.addEventListener("click", (e) => {
  if (e.target !== addEventBtn && !addEventContainer.contains(e.target)) {
    addEventContainer.classList.remove("active");
  }
});

// allow only 50 chars in title
addEventTitle.addEventListener("input", (e)=> {
  addEventTitle.value = addEventTitle.value.slice(0,50);
});
// time format in from and to time

addEventFrom.addEventListener("input", (e)=>{
  addEventFrom.value = addEventFrom.value.replace(/[^0-9:]/g, "");
  // if two numbers enters auto add :
  if(addEventFrom.value.length == 2) {
    addEventFrom.value += ":";
  }
  // dont let user enter more than 5 charecters
  if(addEventFrom.value.length > 5) {
    addEventFrom.value = addEventFrom.value.slice(0, 5);
  }
});

addEventTo.addEventListener("input", (e)=>{
  addEventTo.value = addEventTo.value.replace(/[^0-9:]/g, "");
  // if two numbers enters auto add :
  if(addEventTo.value.length == 2) {
    addEventTo.value += ":";
  }
  // dont let user enter more than 5 charecters
  if(addEventTo.value.length > 5) {
    addEventTo.value = addEventTo.value.slice(0, 5);
  }
});

// function to add listner on days after rendered

function addListner () {
  const days = document.querySelectorAll(".day");
  days.forEach((day) => {
    day.addEventListener("click", (e) => {
      // set current day as active day
      activeDay = Number(e.target.innerHTML);

      // call active day after click
      getActiveDay(e.target.innerHTML);
      updateEvents(Number(e.target.innerHTML) );

      // remove active from already active day
      days.forEach((day) => {
          day.classList.remove("active");
      });

      // if  prev month day clicked goto prev month adn add active
      if(e.target.classList.contains("prev-date")) {
        prevMonth();
        setTimeout(() => {
          // select all days of that month
          const days = document.querySelector(".day");

          // after going to prev month add active to clicked 
          days.forEach((day) => {
            if(!day.classList.contains("prev-date") && day.innerHTML == e.target.innerHTML) {
              day.classList.add("activate");
            }
          })
        }, 100);
        // same with next month days
      } else if(e.target.classList.contains("next-date")) {
        nextMonth();
        setTimeout(() => {
          // select all days of that month
          const days = document.querySelector(".day");

          // after going to prev month add active to clicked 
          days.forEach((day) => {
            if(!day.classList.contains("next-date") && day.innerHTML == e.target.innerHTML) {
              day.classList.add("activate");
            }
          })
        }, 100);
      }
      else {
        // remaining current month days
        e.target.classList.add("active")
      }
    })
  });
}



// lets show active day events and date at top

  
function getActiveDay(date) {
  const day = new Date(year, month, date);
  const dayName = day.toString().split(" ")[0];
  eventday.innerHTML = dayName;
  eventDate.innerHTML = date + " " + months[month] + " " + year;
}


// function to show events for that day

function updateEvents(date) {
  let events = "";
  eventsArr.forEach((event) =>  {
    // got events of active day only
    if (
      date == event.day &&
      month+1 == event.month &&
      year == event.year
    ) {
      // then show event on document
      event.events.forEach((event)  =>{
        events += `<div class="event">
            <div class="title">
              <i class="fas fa-circle"></i>
              <h3 class="event-title">${event.title}</h3>
            </div>
            <div class="event-time">
              <span class="event-time">${event.time}</span>
            </div>
        </div>`;
      });
    }
  });

  // if nothing found
  if (events == "") {
    events = `<div class="no-event">
    <h3>No Events</h3>
    </div>`;
  }
  eventsContainer.innerHTML = events;
  //save events where new one added
  saveEvents();
}

// function to add events 
addEventSubmit.addEventListener("click", ()=> {
  const eventTitle = addEventTitle.value;
  const eventTimeFrom = addEventFrom.value;
  const eventTimeTo =  addEventTo.value;
  var url = "http://"+window.location.hostname+":"+location.port+"/plutocalendar/get_tasks_date_range";
  let formData = new FormData();
  formData.append('startDate', toYearMonthDayFormat(firstDay));  
  formData.append('endDate', toYearMonthDayFormat(lastDay));
  responseDate = "";
  //console.log(firstDay.);
  //console.log(lastDay);
  fetch(url,
   {   method: 'POST',  
   
      body: formData, 
      }
    )  
     .then(function(res){return res.json();})
     .then(function(data){
      //alert(JSON.stringify(data));
      dataProccessed = JSON.parse(JSON.stringify(data));
      //alert("Data proccessed = " + dataProccessed);
      //alert("First obj = " + dataProccessed[0]);
      for(let i = 0; i < dataProccessed.length; i++) {
        //alert("Event added");
        //alert("Object is " + dataProccessed[i]);
        addEvent( dataProccessed[i]);
      }
    })   
     .catch(error => console.error('Error posting data:', error));
  // some validations
  if(eventTitle == "" || eventTimeFrom == "" || eventTimeTo == "") {
    alert("Please fill all the fields");
    return ;
  }

  const timeFromArr = eventTimeFrom.split(":");
  const timeToArr = eventTimeTo.split(":");

  if (
    timeFromArr.length !== 2 ||
    timeToArr.length !== 2 ||
    timeFromArr[0] > 23 ||
    timeFromArr[1] > 59 ||
    timeToArr[0] > 23 ||
    timeToArr[1] > 59
  ) {
    alert("Invalid Time Format");
    return;
  }


  const timeFrom = converTime(eventTimeFrom);
  const timeTo = converTime(eventTimeTo);

  const newEvent = {
    title: eventTitle,
    time : timeFrom + " - " + timeTo,
  };

  let eventAddded = false;

  // check if events are not empty
  if(eventsArr.length > 0) {
    // cehck if current day hasalready any event then add to that
    eventsArr.forEach((item) =>  {
      if(
        item.day == activeDay &&
        item.month == month+1 &&
        item.year == year
      ) {
        item.events.push(newEvent);
        eventAddded = true;
      }
    })
  }

  //if event array empty or current day has not event create new
  if(!eventAddded) {
    eventsArr.push ({
      day: activeDay,
      month: month + 1,
      year: year,
      events: [newEvent],
    });
  }

  // removes active from add event form 
  addEventContainer.classList.remove("active");

  //clear the fields;
  addEventTitle.value = "";
  addEventFrom.value = "";
  addEventTo.value = "";

  // show current added event

  updateEvents(activeDay);

  // also add event class to newly added day if not already 

  const activeDayElem = document.querySelector(".day.active");
  if(!activeDayElem.classList.contains("event")) {
    activeDayElem.classList.add("event")
  }
});

function converTime(time){
  let timeArr = time.split(":");
  let timeHour = timeArr[0];
  let timeMin = timeArr[1];
  let timeFormat = timeHour >= 12 ? "PM" : "AM";
  timeHour = timeHour % 12 || 12;
  time = timeHour + ":" + timeMin + " " + timeFormat;
  return time;
}


// function to remove events on click 

eventsContainer.addEventListener("click", (e) => {
  if(e.target.classList.contains("event")) {
    const eventTitle = e.target.children[0].children[1].innerHTML;

    eventsArr.forEach((event) => {
      if (
        event.day === activeDay &&
        event.month === month + 1 &&
        event.year === year
      ) {
        event.events.forEach((item, index) => {
          if (item.title === eventTitle) {
            event.events.splice(index, 1);
          }
        });

        // if no events remaing on that remove complete day
        if(event.events.length == 0) {
          eventsArr.splice(eventsArr.indexOf(event),1);
          //after remove complete day also remove active class of that day

          const activeDayElem = document.querySelector(".day.active");
          if(activeDayElem.classList.contains("event")) {
            activeDayElem.classList.remove("event")
          }
        }
      }
    });
    // after removing from array update events
    updateEvents(activeDay);
  }
});

//state events in local storage get from there

function saveEvents() {
  localStorage.setItem["events", JSON.stringify(eventsArr)];
}

function getEvents() {
  //check if events are already saved in local storage then return event else nothing
  if (localStorage.getItem("events") === null) {
    return;
  }
  eventsArr.push(...JSON.parse(localStorage.getItem("events")));
}



//sorted using bubble sort
function reorder() {
  
  console.log(eventsArr[0].events)
  console.log(startTime(eventsArr[0].events[0]))
  
  var i, j;
  var len = eventsArr[0].events.length;

  var isSwapped = false;

  for (i = 0; i < len; i++) {

      isSwapped = false;

      for (j = 0; j < (len - i - 1); j++) {
          if (startTime(eventsArr[0].events[j]) > startTime(eventsArr[0].events[j+1])) {
            console.log('switch')
              var temp = eventsArr[0].events[j]
              eventsArr[0].events[j] = eventsArr[0].events[j+1]
              eventsArr[0].events[j+1] = temp;
              isSwapped = true;
          }
      }

      // IF no two elements were swapped
      // by inner loop, then break 
      if (!isSwapped) {
          break;
      }
  }
  updateEvents(activeDay)
  console.log(eventsArr[0].events)
  }
  
  



  reorderButt = document.querySelector(".reorder-events")
reorderButt.addEventListener("click", e => {
  reorder()
})

function startTime(event){
  
  if(event.time.substring(0,8).includes("PM")){
    return Number(event.time.substring(0, 1)) + 12 + (Number(event.time.substring(2, 4)) / 100)
  }
  return Number(event.time.substring(0, 1))
  
}


  






