const form = document.querySelector(".appointment-form");

form.addEventListener("submit", function (event) {

    const firstName = document.getElementById("first-name").value.trim();
    const lastName = document.getElementById("last-name").value.trim();
    const email = document.getElementById("email").value.trim();
    const phone = document.getElementById("phone").value.trim(); 

    const nameRegex = /^[A-Za-z ]{2,50}$/;
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const phoneRegex = /^[0-9]{10}$/;

    let isValid = true;

    if (!nameRegex.test(firstName)) {
        alert("Please enter a valid first name.");
        isValid = false;
    }

    else if (!nameRegex.test(lastName)) {
        alert("Please enter a valid last name.");
        isValid = false;
    }

    else if (!emailRegex.test(email)) {
        alert("Please enter a valid email address.");
        isValid = false;
    }

    else if (!phoneRegex.test(phone)) {
        alert("Please enter a valid 10-digit phone number.");
        isValid = false;
    }

    if (!isValid) {
        event.preventDefault();
    }
});