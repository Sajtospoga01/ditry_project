$(document).ready(function() {
	
	// note - need to find from model whether heart button is liked by current user then can call like functions together
	
	
	
	// toggles colour of heart button is liked/hearted
	
	$('.heartButton').click(function() {
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
	});
	
	
	$('.heartButton').click(function() {
		var id = event.target.id;
		var post = document.getElementById(id);
		var postId = post.getAttribute('id');
		
		$.get('/feed/show_post/${postId}/like-post/',
			function(data) {
				post.html(data);
			}
		)
	});	
	
})
