var gulp = require('gulp');

// Run all tasks by default
gulp.task('default', ['css', 'js', 'icons', 'html']);


// Move index.html
gulp.task('html', function() {
    return gulp.src('src/index.html')
        .pipe(gulp.dest('dist'));
})

// Copy to css/
gulp.task('css', function() {
	return gulp.src(['node_modules/bulma/css/bulma.css', 'node_modules/font-awesome/css/font-awesome.css', 'src/css/app.css'])
		.pipe(gulp.dest('dist/css'));
});

// Copy  to js/
gulp.task('js', function() {
	return gulp.src(['node_modules/jquery/dist/jquery.js', 'node_modules/knockout/build/output/knockout-latest.js', 'src/js/app.js'])
		.pipe(gulp.dest('dist/js'));
});

// Copy to fonts/
gulp.task('icons', function() {
    return gulp.src('node_modules/font-awesome/fonts/**.*')
        .pipe(gulp.dest('dist/fonts'));
});