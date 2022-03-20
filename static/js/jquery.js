$(document).ready(function() {
	
	// toggles whether heart button is liked/hearted
	
	

	
	function like(button) {

		
	}
	
	
	
})


function toggleLiked(postId) {
		var unliked = "/static/images/heart2.png";
		var liked = "/static/images/hearted.png";

		var id = document.getElementById(postId);
		
		if(id.getAttribute('src') == unliked){
			id.setAttribute('src', liked)
			alert("liked")
		}else{
			id.setAttribute('src', unliked)
			alert("unliked")
		}
	}