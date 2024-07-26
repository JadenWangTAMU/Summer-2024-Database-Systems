document.getElementById('sort-by').addEventListener('change', function(){
    document.getElementById('search-form').submit();
});

// JavaScript to hide flashed messages after a certain duration
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(function() {
        var flashes = document.querySelectorAll('.flashes .alert');
        flashes.forEach(function(flash) {
            flash.style.display = 'none';
        });
    }, 10000); // Duration in milliseconds (10000ms = 10 seconds)
});