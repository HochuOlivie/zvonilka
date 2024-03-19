    

    //*********************************************
    //  CHECK THE DEVICE AND BROWSER
    //*********************************************

	    // Control of the functions exists
        $.fn.exists = function () { return this.length > 0; };

        // Check the device for mobile or desktop
        if( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) || $(window).width() < 769 ) { var mobile = true; }
        else{ var mobile = false; }

        // Check the browsers
		// Opera 8.0+
		var isOpera = (!!window.opr && !!opr.addons) || !!window.opera || navigator.userAgent.indexOf(' OPR/') >= 0,
			// Firefox 1.0+
			isFirefox = typeof InstallTrigger !== 'undefined',
			// Safari 3.0+ "[object HTMLElementConstructor]" 
			isSafari = /constructor/i.test(window.HTMLElement) || (function (p) { return p.toString() === "[object SafariRemoteNotification]"; })(!window['safari'] || safari.pushNotification),
			// Internet Explorer 6-11
			isIE = /*@cc_on!@*/false || !!document.documentMode,
			// Edge 20+
			isEdge = !isIE && !!window.StyleMedia,
			// Chrome 1+
			isChrome = /Chrome/.test(navigator.userAgent) && /Google Inc/.test(navigator.vendor),
			// Blink engine detection
			isBlink = (isChrome || isOpera) && !!window.CSS,
			// Parallax effects for selected browsers
			isParallaxBrowsers =  (isOpera || isFirefox || isBlink || isChrome);

        // Add .ie-browser class if browsing with internet explorer.
        if (isIE){ $("body").addClass("ie-browser"); }

    //*********************************************
    //  DETECT RETINA SCREENS
    //*********************************************

        //Detect retina screen type
        function isRetina(){
            return ((window.matchMedia && (window.matchMedia('only screen and (min-resolution: 124dpi), only screen and (min-resolution: 1.3dppx), only screen and (min-resolution: 48.8dpcm)').matches || window.matchMedia('only screen and (-webkit-min-device-pixel-ratio: 1.3), only screen and (-o-min-device-pixel-ratio: 2.6/2), only screen and (min--moz-device-pixel-ratio: 1.3), only screen and (min-device-pixel-ratio: 1.3)').matches)) || (window.devicePixelRatio && window.devicePixelRatio > 1.3));
        }
        //Add .retina-device class to body if the device is retina. And change images for retina screens
        if (isRetina()) { 
            $("body").addClass("retina-device"); 
            $("[data-retina]").each(function(){
                var $this = $(this), $itemWidth = $(this).width(), $rtnIMG = $(this).attr("data-retina");
                $(this).attr("src", $rtnIMG).css({"max-width": $itemWidth + "px"});
            });
        }
        //Add .has-retina-logo class to body if navigation has retina logo
        if ($(".retina-logo").exists()) { $("body").addClass("has-retina-logo"); }

	//*********************************************
    //  NAVIGATION SCRIPTS
    //*********************************************

        //Get Navigation
        var themeNav = $("#navigation"),
            stickyNav = $("#navigation.sticky"),
            hideByScroll = $(".hide-by-scroll");

    	//Call sticky for navigation
        $(stickyNav).sticky({topSpacing:0});
        $('body').scrollspy({ target: ".nav-menu", offset: 200 });

        var position = $(window).scrollTop();

        //Add scrolled class when scroll down
        function getScrolledClass() {
            if ($(window).scrollTop() > 0) { $(themeNav).addClass("scrolled"); }
            else {  $(themeNav).removeClass("scrolled"); }
        } getScrolledClass();

		var scroll = function () {
            var linkParent =  $(".nav-menu").find("a").parents("li"), linkParentActive = $(".nav-menu").find("a.active").parents("li");
            $(linkParent).removeClass("active");
        	$(linkParentActive).addClass("active");

            getScrolledClass();
            var scroll = $(window).scrollTop();
            if (scroll > position - 1 && scroll > 700) {
                $(hideByScroll).addClass('hiding');
            } else {
                $(hideByScroll).removeClass('hiding');
            }
            position = scroll;
            if($(window).scrollTop() + $(window).height() === $(document).height()) {
                $(hideByScroll).removeClass('hiding');
            }
		};

		var waiting = false, endScrollHandle;
		$(window).scroll(function () {
		    if (waiting) { return; }
		    waiting = true;
		    // clear previous scheduled endScrollHandle
		    clearTimeout(endScrollHandle);
		    scroll();
		    setTimeout(function () {
		        waiting = false;
		    }, 50);
		    // schedule an extra execution of scroll() after 200ms
		    // in case the scrolling stops in next 100ms
		    endScrollHandle = setTimeout(function () { scroll(); }, 100);
		});

        //Stay Page when click on "stay" class
        $('.stay').on('click', function(e){ e.preventDefault(); });

        //Dropdown styles
        $('#navigation .has-sub').each(function() {
        	var showMobileNav = 992;
            var $this = $(this);
            //Element over function
            $.fn.elementOver = function() {
                var $this = $(this), $item = $($this).find('>.dropdown-menu');
                if ($(window).width() > showMobileNav) {
                    $($item).stop().show(0);
                    $('#navigation .has-sub').not($this).not($(this).parents('.has-sub')).not($(this).find('.has-sub')).find('.dropdown-menu').stop(true,true).hide(0).parents().removeClass("showing");
                }
                //Check screen sizes, dropdown width and heights
                var navTop = $(themeNav).offset().top,
                    navHeight = $(themeNav).height(),
                    itemTop = ($($item).offset().top - navTop) + navHeight,
                    itemWidth = $($this).outerWidth(),
                    itemHeight = $($item).height(),
                    wHeight = $(window).height(),
                    ofRight = ($(window).width() - ($item.offset().left + $item.outerWidth())),
                    thisRight = ($(window).width() - ($this.offset().left + $this.outerWidth())),
                    ofBottom = ($(window).height() - (itemTop + $item.height()));
                if (ofRight < 30) {
                    if ($($item).hasClass('mega-menu') ) { $($item).addClass('to-left').css({'right': - thisRight + 20 + 'px' });}
                    else {$($item).removeClass('to-right to-center').addClass('to-left');}
                }
                if (ofBottom < 30) {
                    if (!$($item).hasClass('mega-menu')) { $($item).css({'top': (wHeight -  (itemTop + itemHeight)) - 50 + 'px' }) }
                }
                // If mega menu
                if ($($this).find(">.dropdown-menu").hasClass("mega-menu")) {
                    var wWidth = $(window).width(), megaElem = $($this).find(">.mega-menu"), elemWidth = megaElem.width();
                    if (elemWidth >= wWidth - 60) {
                        var colLength = megaElem.find("ul.column").length;
                        megaElem.addClass("too-big");
                    } else{ megaElem.removeClass("too-big"); }
                }
            }
            //Element leave function
            $.fn.elementLeave = function() {
                var $this = $(this), $item = $($this).find('.dropdown-menu');
                if ($(window).width() > showMobileNav) {
                    $($item).stop(true,true).delay(1000).hide(0);
                }
            }
            //Element over function work for desktops
            $(this).on('mouseenter', function(){
                if ($(window).width() > showMobileNav) {
                    $(this).elementOver(); 
                }
            });
            //Element leave function work for desktops
            $(this).on('mouseleave',function(){ 
                if ($(window).width() > showMobileNav) {
                    $(this).elementLeave(); 
                }
            });
            // Close dropdown menu when hover another link
            $('#navigation .nav-links>li:not(.has-sub) a').on('mouseenter', function(){
                if ($(window).width() > showMobileNav) {
                	$('#navigation .dropdown-menu').stop().hide(0);
                }
            });
            //work dropdown for mobile devices
            $(this).find(">a").on("click", function(){
                if ($(window).width() < showMobileNav) {
                    $($this).find('>.dropdown-menu').stop().slideToggle({duration: 400, easing: "easeInOutQuart"}).parent().toggleClass("showing");
                    $('#navigation .has-sub').not($this).not($(this).parents('.has-sub')).not($(this).find('.has-sub')).find('.dropdown-menu').stop(true,true).slideUp({duration: 400, easing: "easeInOutQuart"}).parent(".has-sub").removeClass("showing");
                    return false;
                }
            });
        });

        // add #top href for scroll to top
        $( "a[href='#top']" ).on('click', function() {
            $('html, body').stop().animate({ scrollTop : 0 }, 1400, 'easeInOutExpo');
            return false;
        });

        // Show/Hide mobile navigation
        $('.mobile-nb').on("click", function(){ 
        	$(".navigation .mobile-nav-bg").fadeIn(300); 
        	$('#navigation .nav-menu').addClass("animate");
        	setTimeout( function(){ $('#navigation .nav-menu').addClass("active"); }, 300); 
            return false;
        });
        $('.mobile-nav-bg').on("click", function(){ 
        	$('#navigation .nav-menu').removeClass("active");
        	$(".navigation .mobile-nav-bg").fadeOut(300);
        	$('#navigation li').removeClass("showing");
        	$('#navigation .dropdown-menu').slideUp(300);
        	setTimeout( function(){ $('#navigation .nav-menu').removeClass("animate"); }, 500); 
            return false;
        });

	//*********************************************
    //  FULLSCREEN SEARCH FORM
    //*********************************************

        var trigger = $('.search-form-trigger'),
            form = $('.fs-searchform');
        $(trigger).on('click', function(event){
            $(form).addClass('active');
            setTimeout( function(){$('.fs-searchform input').focus();},900);
            return false;
        });
        $('.form-bg').on('click', function(){
            $('.fs-searchform').removeClass('active');
        });
        //Close the form with press ESC.
        $(document).keyup(function(e) {if (e.keyCode === 27) {$('.fs-searchform').removeClass('active');} });
        $('.fs-searchform a').on('click', function(){
            var Exlink = this.getAttribute('href');
            // Close the navigation
            $('.fs-searchform').removeClass('active');
            setTimeout( function(){ document.location.href = Exlink;},500);
            return false;
        });

	//*********************************************
    //  POPOVERS
    //*********************************************

		//Call popovers
        $('[data-toggle="popover"]').each(function(){
            $(this).popover({html: true, boolean: false });
        });

	//*********************************************
    //  LINE SKILLS
    //*********************************************

        if ($('.line-skills').exists()){
            $('.progress-bar').each(function(){
                var $this = $(this);
                $($this).waypoint(function(){
                    var dataSource = $($this).attr('data-value');
                    $($this).animate({ "width" : dataSource + "%"}, 300);
                    this.destroy();
                }, {offset: '100%'});
            });
        }

    //*********************************************
    //  BACKGROUND IMAGES & COLORS WITH DATA ATTRIBUTES
    //*********************************************

	    //Get Background Image
        $("[data-background]").each(function () {
            var bgSRC = $(this).data('background'), self = $(this);
            $(this).css({'background-image': 'url(' + bgSRC + ')'});
        });
        //Get Background Image for only mobile
        $("[data-mobile-background]").each(function () {
            if (mobile === true & $(window).width() < 769) {
                var mBgSRC = $(this).data('mobile-background'), self = $(this);
                $(this).css({'background-image': 'url(' + mBgSRC + ')'});
            }
        });
        //Get Color
	    $("[data-color]").each(function () {
	        var colorSRC = $(this).data('color'), self = $(this);
	        $(this).css({'color': colorSRC});
	    });
        //Get background color
        $("[data-bgcolor]").each(function () {
            var bgColorSRC = $(this).data('bgcolor'), self = $(this);
            $(this).css({'background-color': bgColorSRC});
        });

    //*********************************************
    //  DETECT DOCUMENT HEIGHT CHANGE
    //*********************************************

    	//Detect changed body height
    	function onElementHeightChange(elm, callback){
		    var lastHeight = elm.clientHeight, newHeight;
		    (function run(){
		        newHeight = elm.clientHeight;
		        if( lastHeight != newHeight )
		            callback();
		        lastHeight = newHeight;
		        if( elm.onElementHeightChangeTimer )
		            clearTimeout(elm.onElementHeightChangeTimer);
		        elm.onElementHeightChangeTimer = setTimeout(run, 200);
		    })();
		}
		//Refresh plugins when document height changed
		onElementHeightChange(document.body, function(){
		    Waypoint.refreshAll();
            if (mobile === false) {
                s.refresh();
            }
		});

	//*********************************************
    //  CALL PARALLAX EFFECT FOR ONLY LARGE SCREENS
    //*********************************************

        var bgParallax = $(".bg-parallax"), bgParallaxParents = $(bgParallax).parents("section");
	    
	    if (mobile === false){
        	//Ready skrollr effects
            var s = skrollr.init({
                forceHeight: false,
                smoothScrolling: false,
            });
            $(bgParallaxParents).addClass("has-parallax");
	    } else{
	    	//Add class for mobile devices
	    	$(bgParallax).addClass('bg-parallax-mobiled').parents("section").addClass("has-parallax");
	    }

	//*********************************************
    //  SKILLS
    //*********************************************

    	var skillBarColor = $(".skill-bar-color").css("background-color");
    	$('.chart').each(function(){
    		var elem = $(this),
    			size = elem.attr("data-size"),
    			elWidth = elem.attr("data-line-width");
    		elem.css({"height": size + "px"});
			$(elem).waypoint(function() {
				$(elem).easyPieChart({
					easing: 'easeInOutExpo',
					barColor: skillBarColor,
					trackColor: 'rgba(127,127,127,0.09)',
					scaleColor: 'transparent',
					scaleLength: 5,
					lineCap: 'round',
					lineWidth: elWidth,
					trackWidth: elWidth,
					size: size,
					rotate: 0,
					animate: {
						duration: 1600,
						enabled: true
					}
				});
			}, {offset: '101%'});
		});

	//*********************************************
    //  WINDOW LOAD FUNCTION START
    //*********************************************

	// Start Function
    (function($, window, document, undefined) {

    	'use strict';

	//*********************************************
    //  HOME PAGE SLIDER
    //*********************************************

    	//Call Swiper Slider For Home V3
	    var swiperHome = new Swiper('.home-slider-container', {
	    	effect: 'fade', // 'slide' or 'fade' or 'cube' or 'coverflow' or 'flip'
	    	speed: 600,
	    	loop: true,
	    	touchRatio: 0,
	    	followFinger: false,
	    	autoplay: {
				delay: 12000,
				disableOnInteraction: false,
			},
	     	navigation: {
				nextEl: '.slider-next',
				prevEl: '.slider-prev',
			},
            on: {
                resize: function () {
                    swiperHome.update();
                }
            }
	    });

	//*********************************************
    //  HOME PAGE TEXT SLIDER
    //*********************************************

		var swiperHometext = new Swiper('.home-text-slider', {
			effect: 'fade',
			initialSlide: 0,
			loop: true,
			speed: 300,
			preventClicksPropagation: false,
			autoplay: {
				delay: 3500,
				disableOnInteraction: false,
			},
			touchRatio: 1,
			autoHeight: true,
			navigation: {
				nextEl: '.home-text-slider-next',
				prevEl: '.home-text-slider-prev',
			},
            on: {
                resize: function () {
                    swiperHometext.update();
                }
            }
		});

    //*********************************************
    //  FEATURES SECTION SLIDER OPTIONS
    //*********************************************
        var featuresSect = $(".features"),
            featuresSlideChanger = $(".features").find("[data-go-slide]"),
		    swiperFeatures = new Swiper('.features-slider', {
    			effect: 'fade',
    			initialSlide: 2,
    			touchRatio: 1,
    			loop: true,
    			autoHeight: true,
    			dynamicBullets: true,
    			pagination: {
    				el: '.features-pagination',
    				clickable: true,
    			},
    			on: {
    				init: function () {
    			        var currentSlide = this.activeIndex;
    					$(featuresSect).find("[data-go-slide='" + currentSlide +"']").addClass("active");
    		        },
    				slideChange: function () {
    					$(featuresSlideChanger).removeClass("active");
    					var currentSlide = this.activeIndex;
    					$(featuresSect).find("[data-go-slide='" + currentSlide +"']").addClass("active");
    		        },
                    resize: function () {
                        swiperFeatures.update();
                    }
    		    }
    		});
		//Change slides with hotspots + $("#features-slider").outerHeight() - $(window).height() 
		$(".features .slide-changer").each(function(){
			$(this).on('click', function (e) {
				var	slideSelect = $(this).data("go-slide"),
					screenCenter = $(window).outerHeight() / 1.7;
				e.preventDefault();
				swiperFeatures.slideTo(slideSelect, 350);
				if ($(window).width() > 1100) {
					$('html, body').animate({ scrollTop : $("#features-texts").offset().top - screenCenter }, 700, 'easeInOutExpo');
				}
                return false;
			});
		});

        //add .inview class to .active-inview elements when visible
        $(".active-inview").each(function(){
            var elem = $(this);
            var inview = new Waypoint.Inview({
                element: $(elem)[0],
                enter: function(direction) {
                    elem.addClass("inview");
                },
                exited: function(direction) {
                    elem.removeClass("inview");
                }
            });
        });

    //*********************************************
    //  HISTORY SECTION - AJAX LOADING
    //*********************************************

    	//When click on load more button
		$('.history-wrapper .load-more-button').on("click", function(ev){
			ev.preventDefault();
            var value = $(this).data("ajax-file"),
                $this = $(this),
                $noMoreBtn = $(".history-wrapper .no-more-button"),
                $last = $(".history-wrapper .note").last(),
                wrapper = $(".history-wrapper"),
                wrapperHeight = $(wrapper).height();
            $(this).html("<img src='images/loading1.svg' alt='loader' />");
            $(wrapper).addClass("news-loading").css({"height": wrapperHeight + "px"});
            //Ready for load new posts
            setTimeout(function(){
	            $(".history-wrapper .news").load(value, function(){
	            	var news = $(".history-wrapper .news").html();
	            	$(news).insertAfter($last);
	            	$(".history-wrapper .news").empty();

            		$($this).fadeOut(150);
					$($noMoreBtn).css({"display": "flex"});

	        		$("body").animatedItems();
	        		var newHeight = $(".history .note-keeper").height()
					$(wrapper).css({"height": newHeight + "px"});
					setTimeout(function(){ $(wrapper).removeClass("news-loading").css({"height": "auto"}); }, 1200);
	            });
        	}, 500);
            return false;
        });


    //*********************************************
    //  TEAM MEMBERS - TRIPLE SLIDER
    //*********************************************

    	//Call Swiper Slider For Home
	    var teamSlider = new Swiper('.team-slider.activated', {
	    	effect: 'coverflow', // 'slide' or 'fade' or 'cube' or 'coverflow' or 'flip'
	    	speed: 600,
	    	loop: true,
	    	touchRatio: 1,
	     	pagination: {
		        el: '.team-pagination',
		        clickable: true,
	      	}
	    });

    //*********************************************
    //  PROJECTS SECTION - CENTERED SLIDER
    //*********************************************
		//Set autoplay delay
		var autoplayDelay = 8500,
            slideTimer = $(".slider-timer");
		//Call project slider
		var projectSlider = new Swiper('.project-slider', {
			initialSlide: 1,
	    	loop: true,
	    	autoplay: {
                enabled: false,
				delay: autoplayDelay,
				disableOnInteraction: false,
			},
	    	speed: 1200,
	    	touchRatio: 1,
	    	followFinger: false,
			slidesPerView: "auto",
			preventInteractionOnTransition: true,
			allowTouchMove: false,
			touchMoveStopPropagation: false,
			touchStartPreventDefault: false,
			centeredSlides: true,
			spaceBetween: 10,
			navigation: {
				nextEl: '.next-project',
				prevEl: '.prev-project',
			},
			breakpoints: {
				768: {
					spaceBetween: 20,
				}
			},
			on: {
				init: function () {
					$(slideTimer).stop().clearQueue().css({"width": 0 + "%"});
				},
				slideChangeTransitionStart: function () {
					$(slideTimer).stop();
				},
				slideChangeTransitionEnd: function () {
					$(slideTimer).stop().animate({"width": 0 + "%"}, 50);
					$(".swiper-slide-active .slider-timer, .swiper-slide-duplicate-active .slider-timer").clearQueue().animate({"width": 100 + "%"}, autoplayDelay);
				},
                resize: function () {
                    projectSlider.update();
                }
			}
	    });
        // Stop autoplay and timer when they are invisible
        $(".project-slider").each(function(){
            var elem = $(this);
            var inview = new Waypoint.Inview({
                element: $(elem)[0],
                enter: function(direction) {
                    $(".swiper-slide-active .slider-timer").animate({"width": 100 + "%"}, autoplayDelay);
                    projectSlider.autoplay.start();
                },
                exited: function(direction) {
                    $(slideTimer).stop().clearQueue().css({"width": 0 + "%"});
                    projectSlider.autoplay.stop();
                }
            });
        });

	//*********************************************
    //  STEPS - SVG OPTIONS
    //*********************************************

    	var orgSVGWidth = $(".steps #org-svg").width(),
    		activeStepW = $(".steps .steps-container .active").attr("data-path-width"),
            coloredSvgWrapper = $(".steps .steps-wrapper div.colored-svg"),
            coloredSVG = $(".steps .colored-svg svg");

    	//Set fake path's width by active step
    	$(coloredSvgWrapper).css({"width": activeStepW});

    	//Keep svgs widths same
    	$(coloredSVG).css({"width": orgSVGWidth + "px"});
    	$(window).resize(function(){
    		var orgSVGWidth = $(".steps #org-svg").width();
    		$(coloredSVG).css({"width": orgSVGWidth + "px"});
    	});
        var nextBtn = $(".steps .steps-navigation button.next"), prevBTN = $(".steps .steps-navigation button.prev")
    	//Change path of colored svg with click on boxes
    	$(".steps .steps-boxes>div").on("click", function(){
            $('[data-toggle="popover"]').not(this).popover("hide");
    		var newW = $(this).attr("data-path-width");
    		$(".steps .steps-boxes>div").removeClass("active");
    		$(this).addClass("active");
    		$(coloredSvgWrapper).css({"width": newW});
    		//Modify navigations
    		var curEl = $(this), nextEl = $(this).next(), prevEl = $(this).prev();
    		if (!nextEl.length) { $(".steps .steps-navigation button.next").attr("disabled", true); } else{ $(nextBtn).attr("disabled", false); }
    		if (!prevEl.length) { $(prevBTN).attr("disabled", true); } else{ $(prevBTN).attr("disabled", false); }
    	});

    	//Steps navigation
    	$(".steps .steps-navigation button").on("click", function(){
    		//hide if a popover is active
    		$('.steps [data-toggle="popover"]').popover("hide");
    		//Get previous and next elements
    		var curEl = $(".steps .steps-boxes>div.active"),
    			nextEl = $(".steps .steps-boxes>div.active").next(),
    			prevEl = $(".steps .steps-boxes>div.active").prev(),
    			fakePath = $(".steps .steps-wrapper div.colored-svg");
    		//Toggle "disabled" for navigation buttons
    		if ($(this).hasClass("next") && !nextEl.next().not(".popover").length) { $(nextBtn).attr("disabled", true); } else{ $(nextBtn).attr("disabled", false); }
    		if ($(this).hasClass("prev") && !prevEl.prev().length) { $(prevBTN).attr("disabled", true); } else{ $(prevBTN).attr("disabled", false); }
    		//Change actives and fake path width 
    		if ($(this).hasClass("next") && nextEl.length) {
				curEl.removeClass("active");
    			nextEl.addClass("active");
    			fakePath.css({"width": nextEl.attr("data-path-width")});
    			if (nextEl.attr('data-toggle') == "popover") { nextEl.popover("show"); }
    		} else if ($(this).hasClass("prev") && prevEl.length ) {
				curEl.removeClass("active");
    			prevEl.addClass("active");
    			fakePath.css({"width": prevEl.attr("data-path-width")});
    			if (prevEl.attr('data-toggle') == "popover") { prevEl.popover("show") }
    		}
    	});

	//*********************************************
    //  CONTACT FORM SCRIPTS
    //*********************************************

        //Input effects
    	$(".contact .contact-input").each(function(){
        	//Focus In
    		$(this).focusin(function(){
    			$(this).parent().addClass("focused");
    		});
        	//Focus out
    		$(this).focusout(function() {
    			if ($(this).val().length === 0) {
					$(this).parent().removeClass('focused');
    			}
			});
    	});
        //If contact form is not visible
    	$('.contact-form').each(function() {
    		var elem = $(this);
	    	$(elem).waypoint(function(direction) {
			    if (direction == 'up') { $( elem ).addClass('unvisible'); }
			    else { $( elem ).removeClass('unvisible'); } $( elem ).toggleClass('unvisible'); 
			}, { offset: '0%' });
		});

        //Contact Form Settings
        var validator = $('.contact-form, .newsletter-form');
        var rnuma = Math.floor(Math.random() * 5);
        var rnumb = Math.floor(Math.random() * 5);
        var sum = rnuma + rnumb;
        $('<textarea id="math" style="display:none;">' + sum + '</textarea>').insertAfter(validator);
        $("#verify-label span").html(rnuma + "+" + rnumb + "= ?");

        // Validate Contact Form
        $(validator).each(function(){
            var sendBtn = $(this).find(':submit'),
                $this = $(this),
                timer = window.setTimeout(3500);

            $(sendBtn).on("click", function(){
            	if ( $($this).hasClass("unvisible") ) {
                	$('html, body').stop().animate({ scrollTop : $($this).offset().top - 70 }, 1000, 'easeInOutExpo');
                }
            });
            // Classic Zeplin Validate
            $(this).validate({
            	ignore: ".ignore",
                rules: {
                    verify: { 
                    	required: true,
                    	equalTo:  "#math"
                    },
                    hiddenRecaptcha: {
                        required: function () {
                            if (grecaptcha.getResponse() === '') {
                                $($this).find('.g-recaptcha').addClass('error_warning');
                                return true;
                            } else {
                                $($this).find('.g-recaptcha').removeClass('error_warning');
                                return false;
                            }
                        }
                    }
                },
                showErrors: function(map, list) {
                    this.currentElements.removeClass("error_warning");
                    $.each(list, function(index, error) {
                        window.clearTimeout(timer);
                        if ($($this).hasClass("contact-form")) {
                        	$($this).parent().find(".error-messages").addClass("show error").removeClass("success");
                        	$($this).addClass("error-message-showing");
                        	window.clearTimeout(timer);
                        }
                        $(error.element).addClass("error_warning");
                    });
                }
            });

        });

    //*********************************************
    //  FOOTER SLIDER
    //*********************************************

    	//Call Swiper Slider For Home
	    var footerSlider = new Swiper('.footer-slider', {
			initialSlide: 2,
	    	effect: 'fade', // 'slide' or 'fade' or 'cube' or 'coverflow' or 'flip'
	    	speed: 800,
			autoHeight: true,
	    	touchRatio: 1,
	    	pagination: {
		        el: '.footer-dots',
		        clickable: true,
	      	},
			on: {
				init: function () {
			        var currentSlide = this.activeIndex + 1;
					$("footer").find("[data-go-slide='" + currentSlide + "']").addClass("active");
		        },
				slideChange: function () {
					$("footer").find("[data-go-slide]").removeClass("active");
					var currentSlide = this.activeIndex + 1;
					$("footer").find("[data-go-slide='" + currentSlide + "']").addClass("active");
		        }
		    }
	    });

	    //Change slides with hotspots
		$("footer .slide-changer").each(function(){
			$(this).on('click', function (e) {
				var	slideSelect = $(this).data("go-slide") - 1;
				e.preventDefault();
				footerSlider.slideTo(slideSelect, 350);
				if ($(window).width() < 992) {
					$('html, body').stop().animate({ scrollTop : $("#footer-slider").offset().top - 70 }, 1000, 'easeInOutExpo');
				}
			});
		});

	//*********************************************
    //  LIGHTBOXES
    //*********************************************

        //Lightbox Gallery Class for containers. All "a" links will work for lightbox with click.
        //Also you can add .no-lightbox claass for no-lightbox links.
        $.fn.callLightboxGallery = function() {
            var lightboxGallery = $(".lightbox-gallery"),
                notLightboxGallery = $('.lightbox-gallery:not(.no-lightbox)');
            $(lightboxGallery).lightGallery({
                selector: 'a:not(.no-lightbox):not(.hiding_item)',
                download: true,
                speed: 400,
                loop: true,
                controls: true,
                thumbWidth: 100,
                thumbContHeight: 100,
                thumbnail: true,
                thumbMargin: 8,
                share: true,
                cssEasing: 'cubic-bezier(0.645, 0.045, 0.355, 1)',
                loadYoutubeThumbnail: true,
                youtubeThumbSize: 'default',
                iframeMaxWidth: '75%',
                loadVimeoThumbnail: true,
                vimeoThumbSize: 'thumbnail_medium',
                youtubePlayerParams: { modestbranding: 1, showinfo: 0, rel: 0, controls: 0 },
                vimeoPlayerParams: { byline : 0, portrait : 0, color : 'A90707' }
            });
            $(notLightboxGallery).addClass('lightboxed');
        }
        if ($(".lightbox-gallery").exists()) { $(window).callLightboxGallery(); }

        //Only .lightbox_selected classes will work in .lightbox_selected container
        $.fn.callLightboxSelected = function() {
            $('.lightbox-selected').lightGallery({
                selector: 'a.lightbox_item:not(.hiding_item)',
                download: true,
                speed: 500,
                loop: true,
                controls: true,
                thumbWidth: 100,
                thumbContHeight: 100,
                thumbMargin: 8,
                thumbnail: true,
                share: true,
                cssEasing: 'cubic-bezier(0.645, 0.045, 0.355, 1)',
                loadYoutubeThumbnail: true,
                youtubeThumbSize: 'default',
                loadVimeoThumbnail: true,
                iframeMaxWidth: '75%',
                vimeoThumbSize: 'thumbnail_medium',
                youtubePlayerParams: { modestbranding: 1, showinfo: 0, rel: 0, controls: 0 },
                vimeoPlayerParams: { byline : 0, portrait : 0, color : 'A90707' }
            });
        }
        if ($(".lightbox-selected").exists()) { $(window).callLightboxSelected(); }

        //You can add .lightbox classes to single elements
        $.fn.callLightbox = function() {
            $('.lightbox').lightGallery({
                selector: 'this',
                download: true,
                thumbWidth: 100,
                thumbContHeight: 100,
                thumbnail: true,
                share: true,
                loadYoutubeThumbnail: true,
                youtubeThumbSize: 'default',
                iframeMaxWidth: '75%',
                loadVimeoThumbnail: true,
                youtubePlayerParams: { modestbranding: 1, showinfo: 0, rel: 0, controls: 0 },
                vimeoPlayerParams: { byline : 0, portrait : 0, color : 'A90707' }
            });
        }
        if ($(".lightbox").exists()) { $(window).callLightbox(); }

                

    //*********************************************
    //  COUNT OPTIONS
    //*********************************************

	    //Count To
        $.fn.countTo = function(options) {
            // merge the default plugin settings with the custom options
            options = $.extend({}, $.fn.countTo.defaults, options || {});
            // how many times to update the value, and how much to increment the value on each update
            var loops = Math.ceil(options.speed / options.refreshInterval), increment = (options.to - options.from) / loops;
            return $(this).each(function() {
                var _this = this, loopCount = 0, value = options.from, interval = setInterval(updateTimer, options.refreshInterval);
                function updateTimer() {
                	value += increment; loopCount++; $(_this).html(value.toFixed(options.decimals).replace(/\B(?=(\d{3})+(?!\d))/g, "."));
                    if (typeof(options.onUpdate) === 'function') { options.onUpdate.call(_this, value); }
                    if (loopCount >= loops) { clearInterval(interval); value = options.to; if (typeof(options.onComplete) === 'function') { options.onComplete.call(_this, value);  } }
                }
            });
        };
        $.fn.countTo.defaults = {
            from: 0,  // the number the element should start at
            to: 100,  // the number the element should end at
            speed: 1000,  // how long it should take to count between the target numbers
            refreshInterval: 100,  // how often the element should be updated
            decimals: 0,  // the number of decimal places to show
            onUpdate: null,  // callback method for every time the element is updated,
            onComplete: null,  // callback method for when the element finishes updating
        };
	    // Count options
        $('.fact').each(function() {
            $(this).waypoint(function() {
                var dataSource = $(this.element).attr('data-source');
                //Count Factors Options
                $(this.element).find('.factor').countTo({
                    from: 0,
                    to: dataSource,
                    speed: 1200,
                    refreshInterval: 25
                });
                this.destroy();
            }, {offset: '100%'});
        });

	//*********************************************
    //  LAZY LOAD
    //*********************************************

	    //Use lazy load with only data-src attribute
        var myLazyLoad = new LazyLoad({
			threshold: 1000,
		    elements_selector: "[data-src]"
		});

	//*********************************************
    //  WORKS FILTER AND PAGINATION OPTIONS
    //*********************************************

        // init Isotope
        var $grid = $('.works-grid').isotope();

		// filter items on button click
		$('[data-filter]').on('click', function() {
			var filterValue = $(this).attr('data-filter');
			$grid.isotope({ filter: filterValue });
			$("[data-filter]").removeClass("active");
			$(this).addClass("active");
            $($grid).find(">*").removeClass("hiding_item");
            $($grid).find(">*").not(filterValue).addClass("hiding_item");
            if ($(".lightbox-gallery").exists()) { $(".lightbox-gallery").data('lightGallery').destroy(true); $(window).callLightboxGallery(); }
            if ($(".lightbox-selected").exists()) { $(".lightbox-selected").data('lightGallery').destroy(true); $(window).callLightboxSelected(); }
            if ($(".lightbox").exists()) { $(".lightbox").data('lightGallery').destroy(true); $(window).callLightbox(); }
            return false;
		});

        // Re-layout isotope when window resizing
		$(window).resize(function(){ $($grid).isotope('layout'); });

		//Hide passive pages
        var passivePages = $(".works .works-grid:not(.active)")
		$(passivePages).addClass("hidden")
		//add active class to button when portfolio init
		var activePageN = $(".works .works-grid.active").attr("data-page"),
            worksPagBtn = $(".works-pagination button"),
            worksPagBtnPrev = $(".works-pagination button.prev"),
            worksPagBtnNext = $(".works-pagination button.next");
		$(".works .works-pagination button[data-page=" + activePageN + "]").addClass("active").attr("disabled", true);
		$(worksPagBtnPrev).attr("data-page", + activePageN - 1);
		$(worksPagBtnNext).attr("data-page", + activePageN + 1);

		//Get each pagination buttons
		$(worksPagBtn).each(function(){
			var elem = $(this),
				inner = elem.attr("data-page");
			//if current page is first, disable prev button
			if ( activePageN = 1 ) { $(".works-pagination button.prev").attr("disabled", true); }
			//click on the pagination buttons
			$(elem).on("click", function(){
				var page = elem.attr("data-page"),
                    currentPage = $(".works .works-grid.active");
				//if there is a page like
				if ($(currentPage).attr("data-page") === page || !$(".works .works-grid[data-page=" + page + "]").exists()) {
					return false;
				} else{
                    var works = $(".works"),
                        worksContainer = $(".works .works-container"),
                        worksGrid = $(".works .works-grid"),
                        worksPage = $(".works .works-grid[data-page=" + page + "]"),
                        worksLoader = $(".works .page-change-loader");
					//Set active and disabled pagination buttons
					$(worksPagBtn).attr("disabled", false).removeClass("active");
					var contHeight = $(worksContainer).outerHeight(); $(worksContainer).css({"height": contHeight + "px"});
					$(".works-pagination button:not(.arrow)[data-page=" + page + "]").addClass("active").attr("disabled", true);
					if ( page == 1 ) { $(worksPagBtnPrev).attr("disabled", true); } else{ $(worksPagBtnPrev).attr("disabled", false); }
					$(".works-pagination .active + .arrow.next").attr("disabled", true);
					//add page values to prev and next buttons
					$(worksPagBtnPrev).attr("data-page", + page - 1);
					$(worksPagBtnNext).attr("data-page", + page + 1);
					//add changing class to works for loader animation
					$(worksLoader).show();
					setTimeout(function(){ $(works).addClass("changing"); }, 10);
					//get current filter
					var filter = $("#filters button.active").attr("data-filter");
					//Scroll to filters
					$('html, body').stop().animate({ scrollTop : $("#filters").offset().top - 70 }, 700, 'easeInOutExpo');
					//Hide other page and active current page
					$(currentPage).addClass("hiding");
					setTimeout(function(){ $(worksGrid).removeClass("active"); }, 1000);
					setTimeout(function(){ $(worksGrid).not(".active").addClass("hidden"); $grid.isotope('destroy'); }, 1400);
					setTimeout(function(){ $(worksPage).removeClass("hidden"); $grid.isotope(); }, 1400);
					setTimeout(function(){ $(worksPage).addClass("active").removeClass("hiding");  }, 1450);
                    setTimeout(function(){ $grid.isotope({ filter: filter }); }, 1450);
					setTimeout(function(){ var currentPage = $(".works .works-grid.active"), wrapperH = $(currentPage).height(); $(worksContainer).css({"height": wrapperH + "px"}); }, 2000);
					setTimeout(function(){ $(works).removeClass("changing"); }, 2250);
					setTimeout(function(){ $(worksLoader).hide(); $(worksContainer).css({"height": "auto"}); }, 2650);
				}
                return false;
			});
		});

    //*********************************************
    //  ANIMATED ITEMS
    //*********************************************

        //Animated Items for desktops
        $.fn.animatedItems = function() {
            var animatedItem = $(".animated");
            if ( $(window).width() > 992 && mobile === false) {
                $(animatedItem).each(function() {
                    var item = $(this), animation = item.data('animation');
                    $(item).waypoint(function() {
                        if ( !item.hasClass('visible') ) {
                            var animationDelay = item.data('animation-delay');
                            if ( animationDelay ) { setTimeout(function(){ item.addClass( animation + " visible" ); }, animationDelay); }
                            else { item.addClass( animation + " visible" ); }
                        }
                    }, {offset: '95%'});
                });
            } else { $(animatedItem).addClass("visible") }
        }
        $("body").animatedItems();

    //*********************************************
    //  SMOOTH SCROLL WITH CLICKS
    //*********************************************

        //See links inside the page for smooth scroll
        $( "a[href^='#']:not([href='#']):not(.no-scroll):not([data-slide]):not([data-toggle])" ).on('click', function(eve) {
            var $anchor = $(this), headerOffset = $('#navigation').data("offset"), $target = $($anchor).attr('href');
            eve.preventDefault();
            if($($target).length){
                if($('#navigation').length){
                    if (!$anchor.parent('.has-sub').length ) {
                        $('html, body').stop().animate({ scrollTop : $($anchor.attr('href')).offset().top - headerOffset + "px" }, 1150, 'easeInOutExpo');
                    } else if (mobile === false) {
                        $('html, body').stop().animate({ scrollTop : $($anchor.attr('href')).offset().top - headerOffset + "px" }, 1150, 'easeInOutExpo');
                    }
                } else{
                        $('html, body').stop().animate({ scrollTop : $($anchor.attr('href')).offset().top }, 700, 'easeInOutExpo');
                }
            }
            return false;
        });

    //*********************************************
    //  DISABLE PAGELOADER
    //*********************************************

        //Fadeout circles before
        $(".pageloader").not(".delay").find(">div").fadeOut(100);
        $(".pageloader.delay>div").delay(450).fadeOut(100);
        //Fadeout all loader
        $(".pageloader").not(".delay").fadeOut(700, function(){ $(this).addClass("stop"); });
        $(".pageloader.delay").delay(500).fadeOut(700, function(){ $(this).addClass("stop"); });
        //Before window unload
        $( "a:not(a[href^='#']):not(a[href^='mailto']):not(a[href^='tel']):not([href='#']):not(.no-scroll):not(.lightbox):not(.lightbox-item):not([data-slide]):not([data-toggle]):not([target]):not(.more-post-button):not([rel]):not(.nl-field-toggle)" ).on('click', function() {
            var Exlink = this.getAttribute('href'), $elem = $(this);
            if(/\.(?:jpg|jpeg|gif|png|mp3|mp4)$/i.test($(this).attr('href'))){} else{
                if ($elem.parents('.lightbox-gallery').length || $elem.parent('.has-sub').length) {} else{
                    $(".pageloader").fadeIn(400);
                    setTimeout(function() {document.location.href = Exlink;}, 450);
                    if (mobile === true || isSafari || isFirefox) {
                        setTimeout(function() {$(".pageloader").hide();}, 1200);
                    }
                    return false;
                }
            }
        });

    //*********************************************
    //  RE-LAYOUT ISOTOPE AND PARALLAX
    //*********************************************

        if (mobile === false) {
            s.refresh();
        }

// End Function
})(jQuery, window, document); //  END START FUNCTION
