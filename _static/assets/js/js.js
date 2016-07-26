jQuery(function($) {
	$(document).ready(function() {

		// cache

		var html			= $('html'),
			$body			= $('body'),
			wWidth 			= $(window).innerWidth(),
			wHeight 		= $(window).innerHeight();

		function baseFx() {

			Chart.defaults.global.responsive = true;

			var ctxHospitality = $( "#chartHospitality" ).get(0);
			if ( typeof ctxHospitality != 'undefined' ) {
				var ctxHospitality = ctxHospitality.getContext( "2d" );
				var chartHospitality = new Chart( ctxHospitality );
				new Chart( ctxHospitality ).Doughnut( dataHospitality, {
                	responsive: true,
                	multiTooltipTemplate: "$<%=addCommas(value)%>"
            	});
			}

			var ctxTravel = $( "#chartTravel" ).get(0);
			if ( typeof ctxTravel != 'undefined' ) {
				var ctxTravel = ctxTravel.getContext( "2d" );
				var chartTravel = new Chart( ctxTravel );
				new Chart( ctxTravel ).Doughnut( dataTravel );
			}

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
		
		function addCommas(nStr){

			nStr += '';
			x = nStr.split('.');
			x1 = x[0];
			x2 = x.length > 1 ? '.' + x[1] : '';
			var rgx = /(\d+)(\d{3})/;

			while (rgx.test(x1)) {
				x1 = x1.replace(rgx, '$1' + ',' + '$2');
			}
			
			return x1 + x2;

		}

	});
});