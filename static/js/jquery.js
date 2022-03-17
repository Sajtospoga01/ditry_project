$(document).ready(function() {
	
	// toggles whether heart button is liked/hearted
	function toggleLiked(button) {
		var unliked = 'images/heart2.png';
		var liked = 'images/hearted.png';
		
		if(button.src='images/heart2.png'){
			button.src='images/hearted.png'
			alert("second")
		}else{
			button.src='images/heart2.png'
			alert("third")
		}
	}
	
	$('#sampleHeart1').click(function() {
		toggleLiked();
	});
	
	
	
})