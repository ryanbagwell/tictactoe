define (require) ->
    $ = require 'jquery'
    _ = require 'underscore'
    Backbone = require 'backbone'

    class TicTacToe extends Backbone.View

        events:
            'click td': 'move'


        initialize: (options) ->
            _.bindAll @, 'move', 'updateBoard', 'handleResponse'

            @gameId = options.gameId

        move: (e) ->

            url = '/' + ['game', @gameId, 'move'].join('/') + '/'

            params =
                symbol: 'o',
                square: $(e.currentTarget).attr 'rel'


            $.post url, params, @handleResponse

        handleResponse: (response, status) ->
            @gameOver(response) if response.status == 'game over'

            @updateBoard(response.board) unless response.result != 'success' and response.status == 'game over'

        updateBoard: (board) ->
            _.each board, (symbol, square) ->
                console.log square, symbol
                @$el.find('td[rel="'+square+'"]').text(symbol)
            , @

        gameOver: (response) ->










