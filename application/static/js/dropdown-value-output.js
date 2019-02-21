var dropdowns = document.querySelectorAll('.dropdown-menu.value-output');
dropdowns.forEach(el => {
    var outputSelector = el.getAttribute('data-value-output');
    var parent = el;

    if (!parent.classList) {
        return;
    }

    while (parent && !parent.querySelector(outputSelector)) {
        parent = parent.parentNode;
    }

    var output = parent.querySelector(outputSelector);

    el.querySelectorAll('.dropdown-item').forEach(item => {
        item.addEventListener('click', function() {
            output.textContent = this.getAttribute('data-value');
        });
    });
});