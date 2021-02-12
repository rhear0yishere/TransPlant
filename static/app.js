$(document).ready(e => {
	e.preventDefault();
	let weatherUrl = 'http://api.openweathermap.org/data/2.5/weather?q=';
	let key = 'f6ba5549f3c639dd270d86edb6493470';
	let city = $('.city').val();

	$.ajax({
		url: `${weatherUrl} ${city} &units=imperial&appid=02e84210a52ed716535f02989864d080`,
		method: 'GET',
		success: response => $('.temp').html(`The weather in ${city} is ${response.main.temp} degrees.`)
	});

	$.getJSON('static/plant.json', function(json) {
		function setHtml(z) {
			let starIcon = `<i class="fas fa-star"></i>`;

			$('.species').html(`Species: ${json[z].species}`);
			$('.difficulty').html(`Level of Difficulty: ${starIcon.repeat(json[z].Difficulty)}`);

			$('.water').html(`Level of Watering: ${starIcon.repeat(json[z].watering)}`);
			$('.plantImage').attr('src', json[z].image);

			$('.previousImage')
				.attr('src', json[z].image)
				.animate(
					{
						'margin-right': '400px',
						width: '400px',
						opacity: '1'
					},
					'slow'
				);
			$('.light').html(`Amount of Light: ${starIcon.repeat(json[z].light)}`);
		}

		function animateImage() {
			$('.plantImage').animate(
				{
					opacity: '0'
				},
				'fast'
			);
			$('.plantImage')
				.hide()
				.attr('src', json[i].image)
				.animate(
					{
						'margin-left': '500px',
						width: '400px',
						opacity: '0'
					},
					'fast'
				);
			$('.plantImage').animate(
				{
					'margin-left': '0px',
					width: '400px',
					opacity: '1'
				},
				'slow'
			);
		}

		let userPlantArray = [];
		//initial plant showing
		let i = 0;
		setHtml(0);
		//navigate thru cards
		$('.yesButton').click((e) => {
            e.preventDefault()
			if (i < json.length) {
				//add plant to saved bbz list
				$('.yasPlants').append(`<li>${json[i].species}`);
				userPlantArray.push(json[i].species);
				$('#userPlants').val(userPlantArray);
				animateImage();
				//go onto next card
				i++;
				setHtml(i);
			} else if (i == json.length) {
				$('.swipedThru').css('display', 'block');
			} else {
				$('.swipedThru').css('display', 'block');
			}
		});
		//thank u next button
		$('.noButton').click(() => {
			animateImage();

			if (i < json.length - 1) {
				i++;
				setHtml(i);
			} else {
				$('.swipedThru').css('display', 'block');
			}
		});
		$('.mySpan').hide();
		$('.editButton').click(function(e) {
			$('.mySpan').show();
		});

		$('.editProfileSpan').hide();
		$('.editProfileButton').click(e => {
			$('.editProfileSpan').show();
			$('.editProfileButton').hide();
		});
	});

	$('#slides').superslides({
		animation: 'fade',
		play: 5000,
		pagination: false
	});

	//smooth scrolling
	$('a[href*="#tutorial"]').on('click', function(e) {
		e.preventDefault();

		$('html, body').animate(
			{
				scrollTop: $($(this).attr('href')).offset().top
			},
			500,
			'linear'
		);
	});
});
