$(function () {

    "use strict";

    var
        // variables for backbone and views
        Word, Update, Stoplist, Ranking, RankingView, UpdateView, StoplistView,
        fox_view, msnbc_view, common_view, update_view, msnbc_stoplist_view, fox_stoplist_view,

        // variables for scroller
        counter     =   0,
        count       =   10,
        eightCommon =   false;

	// Bind the tabs using jQuery Tools
	$("#msnbccolumn ul.tabs").tabs("#msnbccolumn div.panes > div");
	$("#foxcolumn ul.tabs").tabs("#foxcolumn div.panes > div");
	
	// Bind the overlays using jQuery Tools
	$("a[rel]").overlay();

	/*
	 * BACKBONE 
	 */

	////////////// MODELS //////////////
	
	// Each word with its rank and count constitutes the model
	Word = Backbone.Model.extend({
		defaults: {
			rank: 0,
			word: "string",
			count: 0
		}
	});
	
	// The update section pulls in last update
	Update = Backbone.Model.extend({
	    defaults: {
            stoplist: "No current data"
        }
    });
    
    // The stop word lists pull in current stoplists
    Stoplist = Backbone.Model.extend({
        defaults: {
            stoplist: "No current data"
        }
    });

	///////////// COLLECTIONS ///////////////////
	
	// All the words for a site make up a ranking, or the common words with count equal to rank 2.
    Ranking = Backbone.Collection.extend({
		model: Word,

		comparator: function (Word) {
			return Word.get('rank');
		}
	});

	//////////// VIEWS //////////////////////
	
	// A Ranking has its own view
	RankingView = Backbone.View.extend({

		// must set ({ el: $('xxx') }) during view creation

		// Template for each wordBox
		template: _.template("<div class='wordBox'><div class='rank'><h4><%= rank %></h4></div><div class='count'><h4><%= count %></h4></div><div class='word'><h3><%= word %></h3></div></div>"),

		events: {
			"click .wordBox" : "info"
		},

		initialize: function () {
			_.bindAll(this, 'render', 'info'); // all functions that use this

			// Create and fetch the collection
			this.collection = new Ranking();
			this.collection.url = 'rankings/' + this.el.id + ".json";  // set collections url to id of container
			this.collection.fetch({success: this.render });
		},

		// Map each word into the template and append.	
		render: function () {
			var self = this;
			_(this.collection.models).each(function (Word) {
				var temp = self.template(Word.toJSON());
				$(self.el).append(temp);
			});
			if ((this.el.id === "commonWords") && (_.size(this.collection.models)) > 8) { eightCommon = true; }
			return this;
		},

		// Tooltip with the link information for the word.
		info: function () {
			return true;
		}
	});
	
	UpdateView = Backbone.View.extend({
	   
	   // Template for each wordBox
        template: _.template("<span class='update'><%= update %></span>"),
        
        initialize: function () {
            _.bindAll(this, 'render'); // all functions that use this
            // Create and fetch the model
            this.model = new Update();
            this.model.url = 'rankings/' + this.el.id + ".json";  // set collections url to id of container
            this.model.fetch({success: this.render });
        },
	     
        render: function () {
            var temp = this.template(this.model.toJSON());
            $(this.el).append(temp);
            return this;
        }
	});
	
	StoplistView = Backbone.View.extend({
       
       // Template for each wordBox
        template: _.template("<h4><%= stoplist %></h4>"),
        
        initialize: function () {
            _.bindAll(this, 'render'); // all functions that use this
            // Create and fetch the model
            this.model = new Stoplist();
            this.model.url = 'rankings/' + this.el.id + ".json";  // set collections url to id of container
            this.model.fetch({success: this.render });
        },
        
        render: function () {
            var temp = this.template(this.model.toJSON());
            $(this.el).append(temp);
            return this;
        }
    });

	// Create the views
	fox_view = new RankingView({ el: $('#foxWordPane') });
	msnbc_view = new RankingView({ el: $('#msnbcWordPane') });
	common_view = new RankingView({ el: $('#commonWords') });
	update_view = new UpdateView({ el: $('#lastUpdate') });
	msnbc_stoplist_view = new StoplistView({ el: $('#stopWordsMSNBC') });
	fox_stoplist_view = new StoplistView({ el: $('#stopWordsFox') });

    // Scroll Function
	setInterval(function () {

		// Select first word from each pane
		var box1, box2, box3,
		    bigBox1, bigBox2, bigBox3;
		box1 = $("#msnbcWordPane .titleBox + div");
		box2 = $("#foxWordPane .titleBox + div");
		if (eightCommon) { box3 = $("#commonWords .titleBox + div"); }

		// on every 20 counts move the top margin 1 pixel up
		if (counter % 15 === 0) {
		    box1.css("margin-top", count + "px");
		    box2.css("margin-top", count + "px");
		    if (eightCommon) {box3.css("margin-top", count + "px"); }
		    count = count - 1;
		}

		counter = counter + 1;

        // at 650 reset counters, delete word, and add to end
		if (counter === 450) {

			counter = 0;
			count = 10;

            bigBox1 = $("#msnbcWordPane");
            bigBox2 = $("#foxWordPane");
            if (eightCommon) { bigBox3 = $("#commonWords"); }

			box1.remove();
			box2.remove();
			if (eightCommon) { box3.remove(); }

			box1.css("margin-top", "10px");
			box2.css("margin-top", "10px");
			if (eightCommon) { box3.css("margin-top", "10px"); }

			bigBox1.append(box1);
			bigBox2.append(box2);
			if (eightCommon) { bigBox3.append(box3); }
		}
	}, 1);

});

