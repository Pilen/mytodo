
function init(data) {
    console.log("init");
    var initialTodos = data[0];
    var currentFilter = "all";
    initialTodos.map(addTodo);
    filterTodos(currentFilter);

    function icon(closed) {
        // Return HTML code for either a closed or open todo icon
        var icon = closed ? "fa-check-circle-o" : "fa-circle-o";
        return '<i class="status fa fa-3x fa '+icon+'"></i>';
    }

    function addTodo(todo) {
        // Add a todo to the page
        // Does NOT post it to the backend
        todo.node = $('<li class="list-group-item  flex-column align-items-start">'+
                      icon(todo.closed)+
                      // '<div class="w-100">'+
                      ('<div class="d-flex justify-content-between">'+
                       '<h5 class="mb-1">'+todo.title+'</h5>'+
                       '<small>'+todo.created_date+'</small>'+
                       '</div>')+
                      '<i class="delete fa fa-trash" style="float: right;"></i>'+
                      '<p class="mb-1">'+todo.description+'</p>'+
                      // '</div>'+
                      "</li>");
        todo.node.data("todo", todo);
        $("ul").prepend(todo.node);
        filterTodos();
    };

    // Setup ajax for creating Todos
    $("form").submit(function(event) {
        event.preventDefault();
        $.ajax({url: event.currentTarget.action,
                type: "post",
                dataType: "json",
                data: $("form").serialize(),
                success: addTodo,
                error: simpleErrorHandler});
        $("form")[0].reset();
    });

    $("ul.list-group").on("click", "i.status", function(event) {
        var todo = $(event.currentTarget.parentElement).data("todo");
        todo.closed = !todo.closed;
        event.currentTarget.outerHTML = icon(todo.closed);
        var csrf = $("input[name='csrfmiddlewaretoken'").attr("value");
        $.ajax({url:"/api/change",
                type: "post",
                dataType: "json",
                data: {id:todo.id,
                       closed:todo.closed,
                       csrfmiddlewaretoken: csrf},
                // success: function(){console.log("yay");},
                error: simpleErrorHandler});
        filterTodos();
    });

    $("ul.list-group").on("click", "i.delete", function(event) {
        if (confirm("Are you sure you want to delete this todo?")) {
            var todo = $(event.currentTarget.parentElement).data("todo");
            var csrf = $("input[name='csrfmiddlewaretoken'").attr("value");
            $.ajax({url:"/api/delete",
                    type: "post",
                    dataType: "json",
                    data: {id:todo.id,
                           csrfmiddlewaretoken: csrf},
                    success: function(){event.currentTarget.parentElement.remove();},
                    error: simpleErrorHandler});
        }
    });


    $(".filterButtons #showAll").click(filterButton("all"));
    $(".filterButtons #showOpen").click(filterButton("open"));
    $(".filterButtons #showClosed").click(filterButton("closed"));

    function filterButton(filter) {
        return function (event) {
            $(".filterButtons button").removeClass("btn-primary");
            $(event.currentTarget).addClass("btn-primary");
            filterTodos(filter);
        };
    }
    function filterTodos(filter) {
        if (!filter) {
            filter = currentFilter;
        }
        currentFilter = filter;

        var $items = $("li.list-group-item");

        if (filter === "all") {
            $items.show();
        } else {
            $items.map(function(i, item) {
                var todo = $(item).data("todo");
                if ((filter === "closed" && todo.closed) || (filter === "open" && !todo.closed)) {
                    $(item).show();
                } else {
                    $(item).hide();
                }
            });
        }
    }

    function simpleErrorHandler(a, b, c) {
        console.log("ERROR:");
        console.log(a);
        console.log(b);
        console.log(c);
    }
}
$.when($.getJSON("/api/all"), $.ready).done(init);
