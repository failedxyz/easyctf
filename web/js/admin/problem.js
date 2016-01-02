function add_problem(name, category, description, hint, flag, value) {
    $.post("/api/problem/add", {
        name: name,
        category: category,
        hint: hint,
        flag: flag,
        value: value
    }, function(data) {

    })
}
