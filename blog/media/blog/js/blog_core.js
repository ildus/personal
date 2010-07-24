function show_error(message) {
	dojo.byId("response").innerHTML = message;
}

var changing_mode = false

function init_blog() {

	function save_comment(e) {
		e.preventDefault();
        e.stopPropagation();
        
        var data = {
				comment: dojo.byId("edt_comment").value,
				id_article: ARTICLE_ID,
				id_comment: COMMENT_ID
		}
		xhrArgs = {
			url: '/blog/comment/edit/',
			handleAs: 'json',
			content: data,
			load: function(response) {
				if (response.success) {
					xhrArgs2 = {
						url: '/blog/comment/'+response.id_comment+'/',
						handleAs: 'text',
						load: function (response) {
							dojo.place(response, dojo.byId('adding_form'), 'after');
							dojo.destroy(dojo.byId("no_comments"));
						},
						error: function(error) {
							show_error(error);
						}
					}
					dojo.xhrGet(xhrArgs2)
				}
				else {
					show_error("Комментарий не был опубликован");
				}
            },
            error: function(error) {
                show_error("Ошибка связи");
            }
		}
		dojo.xhrPost(xhrArgs);
	}
	
	function change_comment(e) {
		//:TODO: сделать нормальный селект
		if (!changing_mode) {
			div = e.target.parentNode.parentNode.parentNode;
			dojo.empty(div);
			dojo.place(dojo.byId('f_addcomment'), div);
			changing_mode = true;
			dojo.query('.btn_cancel').style('display', 'inline');
		}
	}
	
	function delete_comment(e) {}
	
	dojo.query('.btn_add_comment').onclick(save_comment);	
	//dojo.query('.btn_change_comment').onclick(change_comment);	
	//dojo.query('.btn_delete_comment').onclick(delete_comment);
}

dojo.addOnLoad(init_blog);