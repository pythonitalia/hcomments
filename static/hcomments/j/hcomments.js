function bind(f, scope) {
    function wrapper() {
        return f.apply(scope, arguments);
    }
    return wrapper;
};

hcomments = {
    comments: function(o) {
        this.form = o.form;
        this.wrapper = o.wrapper;
        this.comments = o.comments;
        this.remove = o.remove || '';

        this.form.append('<input type="hidden" name="async" value="1" />');
        var scope = this;
        o.form.ajaxForm({
            error: function(request, textStatus, errorThrown) {
                alert('cannot post your comment');
            },
            success: function(data, textStatus) {
                var data = scope.filterOut($(data));
                if(data) {
                    data
                        .hide()
                        .appendTo(scope.wrapper)
                        .fadeIn("slow");
                    scope.addRemoveLink();
                }
            }
        });
        this.addRemoveLink();
    },
    filterOut: function(c) {
        /*
         * django comment è abbastanza furbo da non inserire due volte lo
         * stesso commento (double posting), quindi c potrebbe avere un id già
         * presente
         */
        return $('#' + c.attr('id')).length == 0 ? c : null
    },
    addRemoveLink: function() {
        if(!this.remove)
            return;
        $('<a href="#" class="remove-comment">Remove this comment</a>')
            .click(bind(this._onRemoveComment, this))
            .appendTo('li.user-comment');
    },
    _onRemoveComment: function(e) {
        e.preventDefault();
        var p = $(e.target).parent('li');
        var id = p.attr('id').split('-')[1];
        $.post(this.remove, { cid: id })
        p.hide("slow", function() { $(this).remove(); });
    }
};
