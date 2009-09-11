hcomments = {
    comments: function(o) {
        this.form = o.form;
        this.wrapper = o.wrapper;
        this.comments = o.comments;

        this.form.append('<input type="hidden" name="async" value="1" />');
        var scope = this;
        o.form.ajaxForm({
            error: function(request, textStatus, errorThrown) {
                alert('cannot post your comment');
            },
            success: function(data, textStatus) {
                $(data)
                    .hide()
                    .appendTo(scope.wrapper)
                    .fadeIn("slow");
            }
        });
    },
    isErrorPage: function(data) {
        var tmp = $(data);
        var errors = $('p.error', tmp).length;
        tmp.remove();
        console.info(errors);
        return errors > 0;
    }
};
