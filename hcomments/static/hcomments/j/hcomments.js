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
        o.form.ajaxForm({
            error: function(request, textStatus, errorThrown) {
                if(request.status == 403)
                    alert('Your comment has been moderated');
                else
                    alert('Cannot post your comment');
            },
            success: bind(function(data, textStatus) {
                var data = this.filterOut($(data));
                if(data) {
                    data
                        .hide()
                        .appendTo(this.wrapper)
                        .fadeIn("slow");
                    this.addRemoveLink(data);
                    this.addReplyLink(data);
                }
            }, this)
        });
        this.addRemoveLink();
        this.addReplyLink();
    },
    filterOut: function(c) {
        /*
         * django comment è abbastanza furbo da non inserire due volte lo
         * stesso commento (double posting), quindi c potrebbe avere un id già
         * presente
         */
        return $('#' + c.attr('id')).length == 0 ? c : null
    },
    addRemoveLink: function(target) {
        if(!this.remove)
            return;
        if(!target)
            target = $('li.user-comment');
        $('<span><a href="#" class="remove-comment">Remove</a> |</span>')
            .click(bind(this._onRemoveComment, this))
            .insertBefore($('strong', target));
    },
    _onRemoveComment: function(e) {
        e.preventDefault();
        var p = $(e.target).parents('li');
        var id = p.attr('id').split('-')[1];
        $.post(this.remove, { cid: id })
        p.hide("slow", function() { $(this).remove(); });
    },
    addReplyLink: function(target) {
        if(!target)
            target = this.comments;
        $('<span><a href="#" class="reply-comment">Reply</a> |</span>')
            .click(bind(this._onReplyComment, this))
            .insertBefore($('strong', target));
    },
    _onReplyComment: function(e) {
        e.preventDefault();
        var p = $(e.target).parents('li');
        if($('form', p).length)
            return;
        $('li.replying form').remove();
        $('li.replying').removeClass('replying');
        p.addClass('replying');
        var id = p.attr('id').split('-')[1];
        var form = this.form.clone();
        $('input[name="parent"]', form).val(id);
        $('<button>Cancel</button>')
            .appendTo($('div.buttons', form))
            .click(function(e) {
                e.preventDefault();
                form.remove();
                p.removeClass('replying');
            });
        form
            .ajaxForm({
                error: function(request, textStatus, errorThrown) {
                    alert('cannot post your comment');
                },
                success: bind(function(data, textStatus) {
                    var data = this.filterOut($(data));
                    if(data) {
                        data
                            .hide()
                            .insertAfter(p)
                            .fadeIn("slow");
                        this.addRemoveLink(data);
                        this.addReplyLink(data);
                    }
                }, this),
                complete: function() {
                    form.remove();
                }
            })
            .appendTo(p);
    }
};