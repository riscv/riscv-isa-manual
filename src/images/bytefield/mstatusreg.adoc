[bytefield]
----
(defattrs :plain [:plain {:font-size 14 :font-family "M+ 1p Fallback" :vertical-align "middle"}])
(def row-height 45 )
(def row-header-fn nil)
(def left-margin 0)
(def right-margin 0)
(def boxes-per-row 33)
(draw-column-headers {:height 20 :font-size 18 :labels (reverse ["" "32" "33" "34" "35" "36" "37" "38" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "62" "63"])})

(draw-box "SD" {:span 1})
(draw-box (text "WPRI" {:font-weight "bold"}) {:span 25})
(draw-box "MBE" {:span 1})
(draw-box "SBE" {:span 1})
(draw-box "SXL[1:0]" {:span 2})
(draw-box "UXL[1:0]" {:span 2})
(draw-box "" {:span 1 :borders {:top :border-unrelated :bottom :border-unrelated}})

(draw-box "1" {:span 1 :borders {}})
(draw-box "25" {:span 25 :borders {}})
(draw-box "1" {:span 1 :borders {}})
(draw-box "1" {:span 1 :borders {}})
(draw-box "2" {:span 2 :borders {}})
(draw-box "2" {:span 2 :borders {}})
(draw-box "" {:span 1 :borders {}})
----