import RoadTraffic.modeUDF
import org.apache.spark.sql.{DataFrame, Dataset, Row}
import org.apache.spark.sql.functions.{col, collect_list, count, max, mean, sum}

object Transformation {
  //todo : make a test unitaire for this function
  def filterTtravelTimeReliability(streamDF: DataFrame) : DataFrame =  {
    return streamDF.filter(col("meanTravelTimeReliability") > 50)
  }

  //todo : make a test unitaire for this function
  def imputationColumnSensCircule(streamDF: DataFrame) : DataFrame = {
    return streamDF.na.fill("Double sens", Seq("sens_circule"))
  }

  //todo : make a test unitaire for this function
  val mode: Seq[String] => String = (values: Seq[String]) => {
    if (values.isEmpty) null
    else values.groupBy(identity).mapValues(_.size).maxBy(_._2)._1
  }



  def myAggregation(streamDF: DataFrame) : DataFrame = {
    val df = streamDF
      .withWatermark("datetime", "1 minute")
      .select(col("denomination"),col("datetime"), col("averageVehicleSpeed"), col("travelTime"), col
      ("travelTimeReliability"), col("trafficStatus"), col("vehicleProbeMeasurement"), col("vitesse_maxi"))
      .groupBy(col("denomination"), col("datetime"))
      .agg(
        count("*").alias("nbTroconPerRoad"),
        sum("vehicleProbeMeasurement").alias("nbVehiculePerRoad"),
        mean("averageVehicleSpeed").alias("meanVitessePerRoad"),
        max("vitesse_maxi").alias("vitesseMaximumPerRoad"),
        mean("travelTime").alias("meanTravelTime"),
        mean("travelTimeReliability").alias("meanTravelTimeReliability"),
        collect_list(col("trafficStatus")).as("trafficStatusList")
      ).coalesce(1)

    return df.select(col("denomination"),col("datetime"),col("nbTroconPerRoad"),col("nbVehiculePerRoad"), col
    ("meanVitessePerRoad"), col("vitesseMaximumPerRoad"), col("meanTravelTime"), col("meanTravelTimeReliability"),
      modeUDF(col("trafficStatusList")).as("stateGeneralTrafic"))
  }
}
