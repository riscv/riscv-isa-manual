[bytefield]
----
(defattrs :plain [:plain {:font-size 14 :font-family "M+ 1p Fallback" :vertical-align "middle"}])
(def row-height 45 )
(def row-header-fn nil)
(def left-margin 0)
(def right-margin 0)
(def boxes-per-row 32)
(draw-column-headers {:height 20 :font-size 18 :labels (reverse ["0" "" "" "3" "4" "5" "6" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "31"])})

(draw-box (text "WPRI" {:font-weight "bold"}) {:span 26})
(draw-box "MBE" {:span 1})
(draw-box "SBE" {:span 1})
(draw-box (text "WPRI" {:font-weight "bold"}) {:span 4})

(draw-box "26" {:span 26 :borders {}})
(draw-box "1" {:span 1 :borders {}})
(draw-box "1" {:span 1 :borders {}})
(draw-box "4" {:span 4 :borders {}})
----