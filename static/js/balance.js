document.addEventListener('DOMContentLoaded', function() {
    Element.prototype.addClass = function(className)
{
	if(!this.classList.contains(className)){
		this.classList.add(className);
	}
};

Element.prototype.removeClass = function(className)
{
	if(this.classList.contains(className)){
		this.classList.remove(className);
	}
};

Array.prototype.first = function()
{
	return this[0];
}

Array.prototype.last = function()
{
	return this[this.length - 1];
}

document.querySelectorAll('.inputslider').forEach(
	(inputslider) => {
		let values = inputslider.dataset.values.split(','),
			value = parseFloat(inputslider.dataset.value),
			unit = '',
			min = parseFloat(values.first()),
			max = parseFloat(values.last()),
			input = inputslider.querySelector('input'),
			area = inputslider.querySelector('.area'),
			knob = inputslider.querySelector('.knob'),
			fill = inputslider.querySelector('.fill');

		if(inputslider.dataset.unit){
			unit = inputslider.dataset.unit;
		}

		values.forEach(
			(value, i) => {
				values[i] = value = parseFloat(value);

				let span = document.createElement('span');
				span.innerText = value + unit;
				span.setAttribute('data-value', value);

				if(i == 0){
					span.addClass('selected');
					input.value = value;
				}

				span.style.left = gsap.utils.mapRange(min, max, 0, 100, value) + '%';

				inputslider.querySelector('.values').appendChild(span);
			}
		);

		Draggable.create(knob, {
				type: 'x',
				edgeResistance: 1,
				bounds: area,
				throwProps: false,
				onDrag: function()
				{
					handleInputslider(this, false);
				},
				onDragEnd: function()
				{
					handleInputslider(this, true);
				}
			}
		);
	}
);

function handleInputslider(instance, snap)
{
	let inputslider = instance.target.closest('.inputslider'),
		fill = inputslider.querySelector('.fill'),
		values = inputslider.dataset.values.split(','),
		min = parseFloat(values.first()),
		max = parseFloat(values.last()),
		xPercent = gsap.utils.mapRange(0, instance.maxX, 0, 100, instance.x),
		relativeValue = gsap.utils.mapRange(0, instance.maxX, min, max, instance.x),
		finalValue = gsap.utils.snap(values, relativeValue),
		snapX = gsap.utils.mapRange(min, max, 0, instance.maxX, finalValue),
		fillWidth = gsap.utils.mapRange(0, instance.maxX, 0, 100, snapX);

	if(snap){
		gsap.to(instance.target, {duration: .2, x: snapX});
		gsap.to(fill, {duration: .2, width: fillWidth + '%'});
	}else{
		values.forEach(
			(value, i) => {
				values[i] = parseFloat(value);
			}
		);

		fill.style.width = xPercent + '%';

		inputslider.querySelectorAll('.values span').forEach(
			(span) => {
				if(parseFloat(span.dataset.value) == finalValue){
					span.addClass('selected');
				}else{
					span.removeClass('selected');
				}
			}
		);

		inputslider.querySelector('input').value = finalValue;
	}
}

var faq = document.getElementsByClassName("faq-box-question");
var i;
for (i = 0; i < faq.length; i++) {
    faq[i].addEventListener("click", function () {
        /* Toggle between adding and removing the "active" class,
        to highlight the button that controls the panel */
        this.classList.toggle("active");
        /* Toggle between hiding and showing the active panel */
        var body = this.nextElementSibling;
        if (body.style.maxHeight === "2000px") {
            body.style.maxHeight = "0px";
        } else {
            body.style.maxHeight = "2000px";
        }
    });
}
});