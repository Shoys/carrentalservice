document.addEventListener('DOMContentLoaded', function() {
    let passwordField = document.getElementById('id_password1');
    if (passwordField) {
        passwordField.onkeyup = checkPassword;
    }
});

function checkPassword() {
    let password = document.getElementById('id_password1').value;
    let minLength = document.getElementById('length');

    minLength.classList.toggle('valid', password.length >= 6);
    minLength.classList.toggle('invalid', password.length < 6);
}
