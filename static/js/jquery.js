$(document).ready(function() {
	
	// toggles whether heart button is liked/hearted
	function toggleLiked(button) {
		var unliked = "/static/images/heart2.png";
		var liked = "/static/images/hearted.png";

		if(button.getAttribute('src') == unliked){
			button.setAttribute('src', liked)
			alert("liked")
		}else{
			button.setAttribute('src', unliked)
			alert("unliked")
		}
	}
	
	$('#sampleHeart1').click(function() {
		toggleLiked(document.getElementById('sampleHeart1'));
	});
	
	$('#sampleHeart2').click(function() {
		toggleLiked(document.getElementById('sampleHeart2'));
	});
	
	$('#sampleHeart3').click(function() {
		toggleLiked(document.getElementById('sampleHeart3'));
	});

	$('#sampleHeart4').click(function() {
		toggleLiked(document.getElementById('sampleHeart4'));
	});	

	$('#sampleHeart5').click(function() {
		toggleLiked(document.getElementById('sampleHeart5'));
	});	

	$('#sampleHeart6').click(function() {
		toggleLiked(document.getElementById('sampleHeart6'));
	});

	$('#sampleHeart7').click(function() {
		toggleLiked(document.getElementById('sampleHeart7'));
	});

	$('#sampleHeart8').click(function() {
		toggleLiked(document.getElementById('sampleHeart8'));
	});
	
	
	
})