/*
 UDACITY RESPONSIVE PROJECT GRUNTFILE
 
 After you have changed the settings under responsive_images
 run this with one of these options:
  "grunt" alone creates a new, completed images directory
  "grunt clean" removes the images directory
  "grunt responsive_images" re-processes images without removing the old ones
*/

module.exports = function(grunt) {

  grunt.initConfig({
    responsive_images: {
      dev: {
        options: {
          engine: 'im',
          sizes: [{
            /* Change these */
            width: '100%',
            quality: 50
          },{
	        width: '50%',
	        quality: 40
          },{
	        width: '25%',
	        quality: 30
          }]
        },

        /*
        You don't need to change this part if you don't change
        the directory structure.
        */
        files: [{
          expand: true,
          src: ['*.{gif,jpg,png}'],
          cwd: 'img-src/',
          dest: 'img/'
        }]
      }
    },

    /* Clear out the images directory if it exists */
    clean: {
      dev: {
        src: ['img'],
      },
    },

    /* Generate the images directory if it is missing */
    mkdir: {
      dev: {
        options: {
          create: ['img',
          'img/fixed']
        },
      },
    },
    
    copy: {
	  files: {
	    cwd: 'img-src/fixed',  // set working folder / root to copy
	    src: '**/*',           // copy all files and subfolders
	    dest: 'img/fixed',    // destination folder
	    expand: true           // required when using cwd
	  }
	}

  });

  grunt.loadNpmTasks('grunt-responsive-images');
  grunt.loadNpmTasks('grunt-contrib-clean');
  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.loadNpmTasks('grunt-mkdir');
  grunt.registerTask('default', ['clean', 'mkdir', 'responsive_images', 'copy']);

};
