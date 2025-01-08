// Открытие модального окна
document.getElementById('openModal').onclick = function() {
    document.getElementById('myModal').style.display = 'block';
}
// Закрытие модального окна
document.getElementById('closeModal').onclick = function() {
    document.getElementById('myModal').style.display = 'none';
}
// Закрытие модального окна при клике вне его
window.onclick = function(event) {
    if (event.target == document.getElementById('myModal')) {
        document.getElementById('myModal').style.display = 'none';
    }
}
