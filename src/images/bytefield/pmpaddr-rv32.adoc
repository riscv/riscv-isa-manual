[bytefield]
----
(defattrs :plain [:plain {:font-family "M+ 1p Fallback" :font-size 24}])
(def row-height 40 )
(def row-header-fn nil)
(def left-margin 200)
(def right-margin 200)
(def boxes-per-row 32)
(draw-column-headers {:height 24 :font-size 24 :labels (reverse ["0" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "31"])})

(draw-box "address[33:2]" {:span 16 :text-anchor "end" :borders {:top :border-unrelated :bottom :border-unrelated :left :border-unrelated}})
(draw-box (text "(WARL)" {:font-size 24 :font-weight "bold"}) {:span 16 :text-anchor "start" :borders{:top :border-unrelated :bottom :border-unrelated :right :border-unrelated}})

(draw-box "32" {:font-size 24 :span 32 :borders {}})
----