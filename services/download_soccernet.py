from SoccerNet.Downloader import SoccerNetDownloader

mySoccerNetDownloader = SoccerNetDownloader(LocalDirectory="data/soccernet")

# Nhãn (annotation cho goal, card, ...)
mySoccerNetDownloader.downloadGames(files=["Labels.json"], split=["train", "valid"])

# Đặc trưng nhẹ trích từ ResNet (đã PCA512)
mySoccerNetDownloader.downloadGames(files=["1_ResNET_TF2_PCA512.npy", "2_ResNET_TF2_PCA512.npy"], split=["train", "valid"])

# Dữ liệu đóng gói cho bài toán Spotting (không cần video)
mySoccerNetDownloader.downloadDataTask(task="spotting-2023", split=["train", "valid"])
