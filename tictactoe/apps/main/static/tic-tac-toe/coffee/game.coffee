define (require) ->
    $ = require 'jquery'
    _ = require 'underscore'
    Backbone = require 'backbone'

    class TicTacToe extends Backbone.View

        initialize: (options) ->

