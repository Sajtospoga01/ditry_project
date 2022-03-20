$(document).ready(function() {
	
	// toggles whether heart button is liked/hearted
	
	
	function toggleLikedColour() {
		var id = event.target.id;
		var post = document.getElementById(id);
		var src = post.getAttribute('src');
		
		var unliked = "/static/images/heart2.png";
		var liked = "/static/images/hearted.png";		
		
		if(src == unliked){
			post.setAttribute('src', liked);
			alert("liked");
		}else{
			post.setAttribute('src', unliked);
			alert("unliked");
		}		
	}
	
	function like(button) {

		
	}
	

	
	$('.heartButton').click(function() {
		toggleLikedColour();
	});

	
	
	
})
