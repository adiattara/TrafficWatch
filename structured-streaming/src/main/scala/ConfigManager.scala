import com.typesafe.config.ConfigFactory

object ConfigManager {

  private val config = ConfigFactory.load("application.conf")


  def getApiUrl: String = config.getString("API.url")
  def getApiOutput: String = config.getString("API.output")



  def getCloudInputStream: String = config.getString("CLOUD-STORAGE.input")
  def getCloudCheckpointPath = config.getString("CLOUD-STORAGE.checkpoint")

  def getAccesKey = config.getString("AWS.accessKey")
  def getAwsSecret = config.getString("AWS.secret")


}
