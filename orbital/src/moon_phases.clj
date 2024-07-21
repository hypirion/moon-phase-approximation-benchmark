(ns moon-phases
  (:require [io.olympos.selene.moon :as moon]
            [cljc.java-time.zoned-date-time :as zdt]
            [cljc.java-time.zone-id :as zid])
  (:import java.time.format.DateTimeFormatter))


(def start (zdt/of 1900 1 1 0 0 0 0 (zid/of "UTC")))
(def stop (zdt/of 2101 1 1 0 0 0 0 (zid/of "UTC")))

(def phase-map {::moon/new 0
                ::moon/first-quarter 1
                ::moon/full 2
                ::moon/last-quarter 3})

;(def dt-fmt (DateTimeFormatter/ofPattern "yyyy-MM-ddThh:mm:ssZ"))

(defn compute [args]
  (let [results (->> (moon/phase-seq start)
                     (filter #(contains? phase-map (:phase %)))
                     (take-while #(zdt/is-before (:time %) stop)))]
    (doseq [{:keys [time phase]} results]
      (println (.format DateTimeFormatter/ISO_INSTANT time) (phase-map phase)))))
