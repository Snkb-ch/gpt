

(function() {

    var width, height, largeHeader, canvas, ctx, points, target, animateHeader = true;

    // Main
    initHeader();
    initAnimation();
    addListeners();

    function initHeader() {
        width = window.innerWidth;
        height = window.innerHeight;
        target = {x: width/2, y: height};

        largeHeader = document.getElementById('large-header');



        canvas = document.getElementById('demo-canvas');
        canvas.width = width;
        canvas.height = height;

        ctx = canvas.getContext('2d');

        // create points
        points = [];
        for(var x = 0; x < width; x = x + width/20) {
            for(var y = 0; y < height; y = y + height/20) {
                var px = x + Math.random()*width/20;
                var py = y + Math.random()*height/20;
                var p = {x: px, originX: px, y: py, originY: py };
                points.push(p);
            }
        }

        // for each point find the 5 closest points
        for(var i = 0; i < points.length; i++) {
            var closest = [];
            var p1 = points[i];
            for(var j = 0; j < points.length; j++) {
                var p2 = points[j]
                if(!(p1 == p2)) {
                    var placed = false;
                    for(var k = 0; k < 5; k++) {
                        if(!placed) {
                            if(closest[k] == undefined) {
                                closest[k] = p2;
                                placed = true;
                            }
                        }
                    }

                    for(var k = 0; k < 5; k++) {
                        if(!placed) {
                            if(getDistance(p1, p2) < getDistance(p1, closest[k])) {
                                closest[k] = p2;
                                placed = true;
                            }
                        }
                    }
                }
            }
            p1.closest = closest;
        }

        // assign a circle to each point
        for(var i in points) {
            var c = new Circle(points[i], 2+Math.random()*2, 'rgba(255,255,255,0.3)');
            points[i].circle = c;
        }
    }

    // Event handling
    function addListeners() {
        if(!('ontouchstart' in window)) {
            window.addEventListener('mousemove', mouseMove);
        }
//        window.addEventListener('scroll', scrollCheck);
//        window.addEventListener('resize', resize);
    }

    function mouseMove(e) {
        var posx = posy = 0;
        if (e.pageX || e.pageY) {
            posx = e.pageX;
            posy = e.pageY;
        }
        else if (e.clientX || e.clientY)    {
            posx = e.clientX + document.body.scrollLeft + document.documentElement.scrollLeft;
            posy = e.clientY + document.body.scrollTop + document.documentElement.scrollTop;
        }
        target.x = posx;
        target.y = posy;
    }

//    function scrollCheck() {
//        if(document.body.scrollTop > height) animateHeader = false;
//        else animateHeader = true;
//    }

//    function resize() {
//        width = window.innerWidth;
//        height = window.innerHeight;
//        largeHeader.style.height = height+'px';
//        canvas.width = width;
//        canvas.height = height;
//    }

    // animation
    function initAnimation() {
        animate();
        for(var i in points) {
            shiftPoint(points[i]);
        }
    }

    function animate() {
        if(animateHeader) {
            ctx.clearRect(0,0,width,height);
            for(var i in points) {
                // detect points in range
                if(Math.abs(getDistance(target, points[i])) < 4000) {
                    points[i].active = 0.3;
                    points[i].circle.active = 0.6;
                } else if(Math.abs(getDistance(target, points[i])) < 20000) {
                    points[i].active = 0.1;
                    points[i].circle.active = 0.3;
                } else if(Math.abs(getDistance(target, points[i])) < 40000) {
                    points[i].active = 0.02;
                    points[i].circle.active = 0.1;
                } else {
                    points[i].active = 0;
                    points[i].circle.active = 0;
                }

                drawLines(points[i]);
                points[i].circle.draw();
            }
        }
        requestAnimationFrame(animate);
    }

    function shiftPoint(p) {
        TweenLite.to(p, 1+1*Math.random(), {x:p.originX-50+Math.random()*100,
            y: p.originY-50+Math.random()*100, ease:Circ.easeInOut,
            onComplete: function() {
                shiftPoint(p);
            }});
    }

    // Canvas manipulation
    function drawLines(p) {
        if(!p.active) return;
        for(var i in p.closest) {
            ctx.beginPath();
            ctx.moveTo(p.x, p.y);
            ctx.lineTo(p.closest[i].x, p.closest[i].y);
            ctx.strokeStyle = 'rgba(156,217,249,'+ p.active+')';
            ctx.stroke();
        }
    }

    function Circle(pos,rad,color) {
        var _this = this;

        // constructor
        (function() {
            _this.pos = pos || null;
            _this.radius = rad || null;
            _this.color = color || null;
        })();

        this.draw = function() {
            if(!_this.active) return;
            ctx.beginPath();
            ctx.arc(_this.pos.x, _this.pos.y, _this.radius, 0, 2 * Math.PI, false);
            ctx.fillStyle = 'rgba(156,217,249,'+ _this.active+')';
            ctx.fill();
        };
    }

    // Util
    function getDistance(p1, p2) {
        return Math.pow(p1.x - p2.x, 2) + Math.pow(p1.y - p2.y, 2);
    }

})();



function showBlock(type) {
        // Hide all blocks
         var buttons = document.querySelectorAll('.homev4-container36');
    buttons.forEach(function(button) {
      button.classList.remove('type-active');
    });
    $('.light').removeClass('light');

    // Add 'type-active' class to the clicked button
    var clickedButton = document.querySelector('[data-type="' + type + '"]');
    clickedButton.classList.add('type-active');
        var faqblocks =  document.getElementsByClassName('faq-block');
        var lightblocks =  document.getElementsByClassName('light-text');
        if (window.innerWidth < 800) {

        var blocks = document.getElementsByClassName('cards');
        }
        else{
        var blocks = document.getElementsByClassName('homev4-container-tasks');
        }
        for (var i = 0; i < blocks.length; i++) {
            blocks[i].style.display = 'none';
        }
        for (var i = 0; i < faqblocks.length; i++) {
            faqblocks[i].style.display = 'none';
        }
        for (var i = 0; i < lightblocks.length; i++) {
            lightblocks[i].style.display = 'none';
        }
         if (window.innerWidth < 800) {

        // Show the selected block
        document.getElementById(type + 'Block').style.display = 'flex';
        }
        else{
        document.getElementById(type + 'Blockwide').style.display = 'flex';
        }
        document.getElementById(type + 'faq').style.display = 'block';
        document.getElementById(type + 'light').style.display = 'block';
        $('.' + type + 'light').addClass('light');

    }

  $(document).ready(function () {
    // Initialize Hammer.js on the container element
    var container = document.querySelector('.container');
    var hammer = new Hammer(container);

    // Handle both click and swipe events
    $('input').on('change', function () {
      $('body').toggleClass('blue');
    });

    // Listen for swipe events
    hammer.on('swipeleft swiperight', function (e) {
      var currentIndex = $('input[name="slider"]:checked').index('input[name="slider"]');
      var totalItems = $('input[name="slider"]').length;

      if (e.type === 'swiperight') {
        currentIndex = (currentIndex - 1 + totalItems) % totalItems;
      } else if (e.type === 'swipeleft') {
        currentIndex = (currentIndex + 1) % totalItems;
      }

      // Trigger change event on the corresponding radio button
      $('input[name="slider"]').eq(currentIndex).prop('checked', true).change();
    });
  });

//  if button-tg clicked send Client ID to django

ym(94971306, 'getClientID', function(clientID) {

  var link = $('.button-tg').attr('href'); // Получаем текущий href
  link += '_'+clientID; // Добавляем clientID к href
  $('.button-tg').attr('href', link); // Обновляем href
});