// Using JQuery
(function() {
    var dynamicLists = document.querySelectorAll('.list-item-auto-increment');
    dynamicLists.forEach(el => {
        var templateSelector = el.getAttribute('data-item-template'), i,
            totalTrackerInput = el.querySelector('input[type=hidden].dynamic-list-length-tracker');

        if (!templateSelector || templateSelector === null) {
            console.error('Invalid template selector!');
            return;
        }

        var items = el.querySelectorAll(templateSelector);

        if (items.length === 0) {
            console.error('Cannot find the template!');
            return;
        }

        var template = items[0].cloneNode(true);

        if (!template || template === null) {
            console.error('Invalid template!');
            return;
        }

        i = items.length;

        var lastItem = items[items.length - 1];
        activateDynamicAdd(lastItem, el, template, i, () => {
            // Callback
        },
        () => {
            if (typeof activateDropdownOutputs === 'function') {
                activateDropdownOutputs();
            }

            items = el.querySelectorAll(templateSelector);

            if (totalTrackerInput && totalTrackerInput !== null) {
                totalTrackerInput.value = items.length;
            }
        });
    });

    function activateDynamicAdd(lastItem, element, template, newIndex, callback, focusCallback) {
        if (lastItem) {
            template.querySelectorAll('input').forEach(el => {
                el.value = '';
                
                var name = el.getAttribute('data-name');
                name = name.replace(/(\[\])/g, '[' + newIndex + ']')
        
                el.name = name;
            });

            var input = lastItem.querySelector('.list-item-auto-increment-trigger-input')
            input.addEventListener('focus', function lastItemFocusEvent() {
                var newItem = template.cloneNode(true);
                element.appendChild(newItem);
                input.removeEventListener('focus', lastItemFocusEvent);
                activateDynamicAdd(newItem, element, template, newIndex + 1, callback, focusCallback);

                if (typeof focusCallback === 'function') {
                    focusCallback();
                }
            });

            if (typeof callback === 'function') {
                callback();
            }
        }
    }
}());