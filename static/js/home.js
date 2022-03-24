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

	resizeWindow();


	$(window).resize(function(){
		resizeWindow();
	})



})

// currently just prints out estimated no. columns
function resizeWindow(){
	var pictureWidth = 460;
	var windowWidth = $(window).width();

	if( windowWidth < pictureWidth){
		alert('1 column needed');
	}else if( windowWidth < pictureWidth*2){
		alert ('2 columns needed');
	}else if( windowWidth < pictureWidth*3){
		alert ('3 columns needed');
	}else if( windowWidth < pictureWidth*4){
		alert ('4 columns needed');
	}else if( windowWidth < pictureWidth*5){
		alert ('5 columns needed');
	}
}