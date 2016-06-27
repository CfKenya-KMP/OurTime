jQuery(function($) {
	$(document).ready(function() {

		// cache

		var html			= $('html'),
			$body			= $('body'),
			wWidth 			= $(window).innerWidth(),
			wHeight 		= $(window).innerHeight();

		function baseFx() {

			$(window).load(function() {

				// remove preload class
				$body.removeClass('preload');

			}); // load
		}



		/* On Doc Ready --------------------------------------*/

		// run base functions 
		baseFx();

		// run page functions
		// if ($body.hasClass('home')) { homeFx(); }



		/* On Window Resize ----------------------------------*/

		$(window).resize(function() {

			wWidth = $(window).innerWidth();
			wHeight = $(window).innerHeight();

		});


		/* Abstracted Functions ------------------------------*/

		// activate email links

		function activateEmail (selector) {
			$(selector).html( function() {
				var adr = $(this).data('address');
				var dom = $(this).data('domain');
				var ext = $(this).data('ext');
				return adr + '@' + dom + ext;
			}).attr('href', function() {
				return 'mailto:' + $(this).html();
			}).attr('target', '_blank');
		}
		
	});
});