[bytefield]
----
(defattrs :plain [:plain {:font-family "M+ 1p Fallback"}])
(def row-height 45)
(def row-header-fn nil)
(def boxes-per-row 32)
(draw-column-headers {:height 20 :font-size 18 :labels (reverse ["" "0" "" "1" "" "2" "" "3" "" "7" "" "8" "" "" "9" "" "10" "" "" "" "31" "32" "" "33" "34" "" "" "" "" "" "" "63"])})

(draw-box (text "WPRI" {:font-weight "bold"}) {:span 8})
(draw-box "PMM" {:span 3})
(draw-box (text "WPRI" {:font-weight "bold"}) {:span 5})
(draw-box "SSEED" {:span 3})
(draw-box "USEED" {:span 3})
(draw-box (text "WPRI" {:font-weight "bold"}) {:span 3})
(draw-box "RLB" {:span 2})
(draw-box "MMWP" {:span 3})
(draw-box "MML" {:span 2})

(draw-box "30" {:span 8 :borders {}})
(draw-box "2" {:span 3 :borders {}})
(draw-box "22" {:span 5 :borders {}})
(draw-box "1" {:span 3 :borders {}})
(draw-box "1" {:span 3 :borders {}})
(draw-box "5" {:span 3 :borders {}})
(draw-box "1" {:span 2 :borders {}})
(draw-box "1" {:span 3 :borders {}})
(draw-box "1" {:span 2 :borders {}})
----
