function login() {
    const userName = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    console.log(userName);
    console.log(password);
}

function signup() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const email = document.getElementById('email').value;
    const phone = document.getElementById('phone').value;

    console.log('Sign Up attempt:');
    console.log('Username:', username);
    console.log('Password:', password);
    console.log('Email:', email);
    console.log('Phone Number:', phone);

    // You can add user registration logic here, e.g., store in a database
}