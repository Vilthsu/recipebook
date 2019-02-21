// Using JQuery
var dynamicLists = document.querySelectorAll('.list-item-auto-increment');
dynamicLists.forEach(el => {
    var templateSelector = el.getAttribute('data-item-template');

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

    var lastItem = items[items.length - 1];
    activateDynamicAdd(lastItem, el, template);
});

function activateDynamicAdd(lastItem, element, template) {
    if (lastItem) {
        var input = lastItem.querySelector('.list-item-auto-increment-trigger-input')
        input.addEventListener('focus', function lastItemFocusEvent() {
            var newItem = template.cloneNode(true);
            element.appendChild(newItem);
            input.removeEventListener('focus', lastItemFocusEvent);
            activateDynamicAdd(newItem, element, template);
        });
    }
}