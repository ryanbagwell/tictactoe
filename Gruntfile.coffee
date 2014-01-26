path = require 'path'

module.exports = (grunt) ->
  _ = grunt.util._


  # Used instead of "ext" to accommodate filenames with dots. Lots of
  # talk all over GitHub, including here: https://github.com/gruntjs/grunt/pull/750
  coffeeRename = (dest, src) -> path.join dest, "#{ src.replace /\.(lit)?coffee$/, '.js' }"

  # Project configuration.
  grunt.initConfig
    pkg: grunt.file.readJSON 'package.json'

    coffee:
      compile:
        options:
          sourceMap: true
        files: [
          expand: true
          cwd: 'app/static/<%= _.slugify(projectName) %>/coffee'
          src: ['**/*.?(lit)coffee']
          dest: 'app/static/<%= _.slugify(projectName) %>/js/'
          rename: coffeeRename
        ]

    less:
      compile:
        files: [
          expand: true
          cwd: './app/static/<%= _.slugify(projectName) %>/less/'
          src: ['**/*.less', '!**/_*.less']
          dest: './app/static/<%= _.slugify(projectName) %>/css/'
          ext: '.css'
        ]

    watch:
      options:
        atBegin: true
      coffee:
        files: ['app/static/<%= _.slugify(projectName) %>/coffee/*.?(lit)coffee']
        tasks: ['coffee']
      less:
        files: ['app/static/<%= _.slugify(projectName) %>/less/**/*.less']
        tasks: ['less']

    cssmin:
      minify:
        expand: true
        cwd: 'app/static/<%= _.slugify(projectName) %>/css/'
        src: ['*.css']
        dest: 'app/static/<%= _.slugify(projectName) %>/css/'
        ext: '.css'
        options:
          keepSpecialComments: 0
          banner: '/* <%= projectName %> created by HZDG */'

    uglify:
      all:
        options:
          mangle:
            except: ['require']
        files: [{
          expand: true
          cwd: 'app/static/<%= _.slugify(projectName) %>/js'
          src: ['*.js']
          dest: 'app/static/<%= _.slugify(projectName) %>/js'
        }]


    imagemin:
      all:
        files: [{
          expand: true
          cwd: 'app/static/<%= _.slugify(projectName) %>/img'
          src: ['*.{png,jpg,gif}']
          dest: 'app/static/<%= _.slugify(projectName) %>/img'
        }]


  # Load grunt plugins
  grunt.loadNpmTasks 'grunt-contrib-less'
  grunt.loadNpmTasks 'grunt-contrib-coffee'
  grunt.loadNpmTasks 'grunt-contrib-watch'
  grunt.loadNpmTasks 'grunt-contrib-cssmin'
  grunt.loadNpmTasks 'grunt-contrib-uglify'
  grunt.loadNpmTasks 'grunt-contrib-imagemin'

  # Define tasks.
  grunt.registerTask 'build', ['less', 'coffee',]
  grunt.registerTask 'build:production', ['less', 'coffee', 'cssmin:all', 'uglify:all', 'imagemin:all']
  grunt.registerTask 'default', ['build']