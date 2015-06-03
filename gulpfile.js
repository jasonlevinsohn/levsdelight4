var gulp = require('gulp');
var concat = require('gulp-concat');
var less = require('gulp-less');


gulp.task('less', function() {
    gulp.src('levsdelight_app/static/src/less/*.less')
        .pipe(less())
        .pipe(concat('all.css'))
        .pipe(gulp.dest('levsdelight_app/static/build/css'));
});

gulp.task('watch', function() {
    var watcher,
        filename;
    
    watcher = gulp.watch('levsdelight_app/static/src/less/*.less', ['less']);
    watcher.on('change', function(event) {
        filename = event.path.split('/').pop();
        console.log('File ' + filename + ' was ' + event.type + ', running tasks...');
    });
});

gulp.task('default', ['less', 'watch']);
