
var todos = [];

function init(data) {
    console.log("init");
    var initialTodos = data[0];
    initialTodos.map(addTodo);
    sortTodos();

    function icon(closed) {
        // Return HTML code for either a closed or open todo icon
        var icon = closed ? "fa-check-square-o" : "fa-square-o";
        return '<i class="fa fa-3x fa-fw '+icon+'" style="float: right;"></i>';
    }

    function addTodo(todo) {
        // Add a todo to the page
        // Does NOT post it to the backend

        console.log("addTodo");
        todo.node = $('<li class="list-group-item  flex-column align-items-start">'+
                      ('<div class="d-flex w-100 justify-content-between">'+
                       '<h5 class="mb-1">'+todo.title+'</h5>'+
                       '<small>'+todo.created_date+'</small>'+
                       '</div>')+
                      icon(todo.closed)+
                      '<p class="mb-1">'+todo.description+'</p>'+
                      "</li>");
        todo.node.data("todo", todo);
        $("ul").prepend(todo.node);
        todos.push(todo);
        sortTodos();
    };

    // Setup ajax for creating Todos
    $("form").submit(function(event) {
        event.preventDefault();
        $.ajax({url: event.currentTarget.action,
                type: "post",
                dataType: "json",
                data: $("form").serialize(),
                success: addTodo,
                error: errorhandler});
    });

    $("ul.list-group").on("click", "i", function(event) {
        console.log("click");
        _e = event;
        var todo = $(event.currentTarget.parentElement).data("todo");
        todo.closed = !todo.closed;
        event.currentTarget.outerHTML = icon(todo.closed);
        csrf = $("input[name='csrfmiddlewaretoken'").attr("value");
        $.ajax({url:"/todo/change",
                type: "post",
                dataType: "json",
                data: {id:todo.id,
                       closed:todo.closed,
                       csrfmiddlewaretoken: csrf},
                success: function(){console.log("yay");},
                error: errorhandler});
    });

    function sortTodos() {

    }
}

function errorhandler(a, b, c) {
    console.log("ERROR:");
    console.log(a);
    console.log(b);
    console.log(c);
}

$.when($.getJSON("/todo/all"), $.ready)
    .done(init);
// $().ready(init);
