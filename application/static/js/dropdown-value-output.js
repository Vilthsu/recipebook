function activateDropdownOutputs() {
    var dropdowns = document.querySelectorAll('.dropdown-menu.value-output');
    dropdowns.forEach(el => {
        var outputSelector = el.getAttribute('data-value-output');
        var inputSelector = el.getAttribute('data-value-input'); // Save value to input[type=hidden]
        var parent = el;

        if (!parent.classList) {
            return;
        }

        while (parent && !parent.querySelector(outputSelector)) {
            parent = parent.parentNode;
        }

        var output = parent.querySelector(outputSelector),
            input = parent.querySelector(inputSelector);

        el.querySelectorAll('.dropdown-item').forEach(item => {
            item.addEventListener('click', function() {
                output.textContent = this.getAttribute('data-value');

                if (input && input !== null) {
                    input.value = this.getAttribute('data-value');
                }
            });
        });
    });
}

document.addEventListener("DOMContentLoaded", activateDropdownOutputs);