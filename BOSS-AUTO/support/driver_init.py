from selenium import webdriver


def init_driver():
    edge_options = webdriver.EdgeOptions()
    # MAC
    # edge_options.add_argument('user-data-dir=/Users/frank/Library/Application Support/Microsoft Edge/Default')
    # PC 龚
    # edge_options.add_argument("user-data-dir=C:\\Users\\jennifer\\AppData\\Local\\Microsoft\\Edge\\User Data1")
    # PC 朱 台式机
    edge_options.add_argument("user-data-dir=C:\\Users\\Zhumi\\AppData\\Local\\Microsoft\\Edge\\User Data1")
    # Surface 朱
    # edge_options.add_argument("user-data-dir=C:\\Users\\Zhumi\\AppData\\Local\\Microsoft\\Edge\\User Data Boss")
    driver = webdriver.Edge(options=edge_options)
    return driver