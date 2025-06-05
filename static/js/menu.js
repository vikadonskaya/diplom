document.querySelector('.js-menu-toggle').addEventListener('click', function (e) {
    e.preventDefault();
    document.getElementById('side-menu').classList.toggle('open');
});

document.querySelector('.has-children').addEventListener('click', function (e) {
    e.preventDefault();
    document.getElementById('two-menu').classList.toggle('open');
});

// Закрытие меню при клике вне его
document.addEventListener('click', function (e) {
    const sideMenu = document.getElementById('side-menu');
    const twoMenu = document.getElementById('two-menu');

    // Проверяем, кликнули ли мы вне side-menu
    if (!sideMenu.contains(e.target) && !document.querySelector('.js-menu-toggle').contains(e.target)) {
        sideMenu.classList.remove('open');
    }

    // Проверяем, кликнули ли мы вне two-menu
    if (!twoMenu.contains(e.target) && !document.querySelector('.has-children').contains(e.target)) {
        twoMenu.classList.remove('open');
    }
});
