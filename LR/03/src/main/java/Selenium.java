import io.github.bonigarcia.wdm.WebDriverManager;
import org.apache.commons.lang3.ObjectUtils;
import org.openqa.selenium.*;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.w3c.dom.Document;
import java.io.File;
import java.io.IOException;
import java.util.*;
import java.util.concurrent.TimeUnit;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;

public class Selenium {
    private static final String FILENAME = "Repository.xml";
    public static WebDriver driver=null;
    private String result ="";
    public  String Repository;// Ссылка на репозитори
    public  String variant; // Номер варика
    private String itog_ozenka="0";
    private boolean empty=false;
    private String Var_Repository; // 1 Варик- Лосяш, 2 - Крош и тд

    public Selenium (String Repository,String variant){
        this.Repository=Repository;
        this.variant=variant;
        WebDriverManager.chromedriver().version("80.0.3987.106").setup();
        ChromeOptions options = new ChromeOptions();

        options.setPageLoadStrategy(PageLoadStrategy.NORMAL);
        options.addArguments("--headless");
        options.addArguments("start-maximized");
        options.addArguments("enable-automation");
        options.addArguments("--no-sandbox");
        options.addArguments("--disable-infobars");
        options.addArguments("--disable-dev-shm-usage");
        options.addArguments("--disable-browser-side-navigation");
        options.addArguments("--disable-gpu");

        driver = new ChromeDriver(options);
        driver.manage().timeouts().implicitlyWait(15, TimeUnit.SECONDS);
        driver.manage().timeouts().pageLoadTimeout(15, TimeUnit.SECONDS);
        driver.manage().timeouts().setScriptTimeout(15, TimeUnit.SECONDS);
        Get_GoodReposotory();
        driver.get(Var_Repository);
        Add_Tab();
        Change_Tab(0);
    }

    private void Get_GoodReposotory(){
        try {
            final File xmlFile = new File(System.getProperty("user.dir") + File.separator + FILENAME);
            DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
            DocumentBuilder db = dbf.newDocumentBuilder();
            Document doc = db.parse(xmlFile);

            doc.getDocumentElement().normalize();

            NodeList NodeList = doc.getElementsByTagName("variant");

            for (int i = 0; i < NodeList.getLength(); i++) {
                // Вывoдиm инфopmaцию пo kaждomy из нaйдeнных элemeнтoв
                Node node = NodeList.item(i);
                if (Node.ELEMENT_NODE == node.getNodeType()) {
                    Element element = (Element) node;
                    if (element.getAttribute("id").equals(variant)){
                        Var_Repository=element.getElementsByTagName("url").item(0).getTextContent();
                        break;
                    }
                }
            }
        }
        catch (ParserConfigurationException| SAXException | IOException ex){
            Logger.getLogger(Selenium.class.getName()).log(Level.SEVERE,null,ex);
        }
    }

    public String Get_Result(){
        return result;
    }

    public String Get_Ozenka(){
        return itog_ozenka;
    }

    public String Check_Branches(int Good_branches, int Var_branches) {
        if (Good_branches==Var_branches){  //Если кол-во веток в репозитория одно и тоже то смотрим их имена
            driver.get(Var_Repository+"/branches");
            String Good_branches_Name=pull_String("//div[2]/ul[1]/li[@class='Box-row position-relative' and 1]/branch-filter-item-controller[@class='d-flex flex-items-center Details' and 1]/div[1]/a[@class='branch-name css-truncate-target v-align-baseline width-fit mr-2 Details-content--shown' and 1]",true);
            String good_name=Good_branches_Name;
            Change_Tab(1);
            driver.get(Repository+"/branches");
            String Var_branches_Name=pull_String("//div[2]/ul[1]/li[@class='Box-row position-relative' and 1]/branch-filter-item-controller[@class='d-flex flex-items-center Details' and 1]/div[1]/a[@class='branch-name css-truncate-target v-align-baseline width-fit mr-2 Details-content--shown' and 1]",true);
            Change_Tab(0);
            if (Good_branches_Name.equals(Var_branches_Name)){ //Если с имена все ок, то смотрим кол-во файлов в ветке
                driver.get(Var_Repository+"/tree/master");
                List<WebElement> Good_File_Size =driver.findElements(By.className("js-navigation-item"));
                Change_Tab(1);
                driver.get(Repository+"/tree/master");
                List<WebElement> Var_File_Size =driver.findElements(By.className("js-navigation-item"));
                Change_Tab(0);
                if (Good_File_Size.size()==Var_File_Size.size()){ //Если с кол-во файлов все ок, то смотрим имена этих файлов
                    Good_File_Size=driver.findElements(By.className("content"));
                    String[] Good_File_Str_Mas =new String[Good_File_Size.size()];
                    for (int i=1;i<Good_File_Size.size();i++){
                        Good_File_Str_Mas[i]=Good_File_Size.get(i).getAttribute("textContent");
                        Good_File_Str_Mas[i]=Good_File_Str_Mas[i].replaceAll(" ","").replaceAll("\n","");
                    }
                    Change_Tab(1);
                    Var_File_Size=driver.findElements(By.className("content"));
                    String[] Var_File_Str_Mas =new String[Var_File_Size.size()];
                    for (int i=1;i<Var_File_Size.size();i++){
                        Var_File_Str_Mas[i]=Var_File_Size.get(i).getAttribute("textContent");
                        Var_File_Str_Mas[i]=Var_File_Str_Mas[i].replaceAll(" ","").replaceAll("\n","");
                    }
                    Change_Tab(0);
                    if (Arrays.equals(Good_File_Str_Mas, Var_File_Str_Mas)) { //Если имена файлов в ветках совпадают, то смторим что в этих файлах
                        boolean correct_file = true;
                        for (int i = 1; i < Good_File_Size.size(); i++) { //начинать с 1!!
                            driver.get(Var_Repository + "/blob/master/" + Good_File_Str_Mas[i]);
                            driver.findElement(By.xpath("//a[@id='raw-url']")).click();
                            Good_branches_Name = driver.findElement(By.cssSelector("body")).getAttribute("textContent").replaceAll(" ", "").replaceAll("\n", "").toLowerCase();
                            Change_Tab(1);
                            driver.get(Repository + "/blob/master/" + Var_File_Str_Mas[i]);
                            if (driver.findElements(By.xpath("//a[@id='raw-url']")).size()!=0) {
                                driver.findElement(By.xpath("//a[@id='raw-url']")).click();
                            }
                            else { return "В ветке master неверный тип файла/файлов\n"; }
                            Var_branches_Name = driver.findElement(By.cssSelector("body")).getAttribute("textContent").replaceAll(" ", "").replaceAll("\n", "").toLowerCase();
                            Change_Tab(0);
                            if (!Good_branches_Name.equals(Var_branches_Name)) {
                                correct_file = false;
                            }
                        }
                        if (correct_file) { //Если проверка прошла, то смотрим другую ветку?
                            driver.get(Var_Repository + "/tree/" + good_name);
                            Good_File_Size = driver.findElements(By.className("js-navigation-item"));
                            Change_Tab(1);
                            driver.get(Repository + "/tree/" + good_name);
                            Var_File_Size = driver.findElements(By.className("js-navigation-item"));
                            Change_Tab(0);
                            if (Good_File_Size.size() == Var_File_Size.size()) { //Если с кол-во файлов все ок, то смотрим имена этих файлов
                                Good_File_Size = driver.findElements(By.className("content"));
                                Good_File_Str_Mas = new String[Good_File_Size.size()];
                                for (int i = 1; i < Good_File_Size.size(); i++) {
                                    Good_File_Str_Mas[i] = Good_File_Size.get(i).getAttribute("textContent");
                                    Good_File_Str_Mas[i] = Good_File_Str_Mas[i].replaceAll(" ", "").replaceAll("\n", "");
                                }
                                Change_Tab(1);
                                Var_File_Size = driver.findElements(By.className("content"));
                                Var_File_Str_Mas = new String[Var_File_Size.size()];
                                for (int i = 1; i < Good_File_Size.size(); i++) {
                                    Var_File_Str_Mas[i] = Var_File_Size.get(i).getAttribute("textContent");
                                    Var_File_Str_Mas[i] = Var_File_Str_Mas[i].replaceAll(" ", "").replaceAll("\n", "");
                                }
                                Change_Tab(0);
                                if (Arrays.equals(Good_File_Str_Mas, Var_File_Str_Mas)) { //Если имена файлов в ветках совпадают, то смторим что в этих файлах
                                    correct_file = true;
                                    for (int i = 1; i < Good_File_Size.size(); i++) { //начинать с 1!!
                                        driver.get(Var_Repository + "/blob/" + good_name + "/" + Good_File_Str_Mas[i]);
                                        driver.findElement(By.xpath("//a[@id='raw-url']")).click();
                                        Good_branches_Name = driver.findElement(By.cssSelector("body")).getAttribute("textContent").replaceAll(" ", "").replaceAll("\n", "").toLowerCase();
                                        Change_Tab(1);
                                        driver.get(Repository + "/blob/" + good_name + "/" + Var_File_Str_Mas[i]);
                                        if (driver.findElements(By.xpath("//a[@id='raw-url']")).size()!=0) {
                                            driver.findElement(By.xpath("//a[@id='raw-url']")).click();
                                        }
                                        else { return "В ветке "+good_name+" неверный тип файла/файлов\n"; }
                                        Var_branches_Name = driver.findElement(By.cssSelector("body")).getAttribute("textContent").replaceAll(" ", "").replaceAll("\n", "").toLowerCase();
                                        Change_Tab(0);
                                        if (!Good_branches_Name.equals(Var_branches_Name)) {
                                            correct_file = false;
                                        }
                                    }
                                    if (correct_file) {
                                        return "";
                                    }
                                    else { return "Наполнение файлов в ветке " + good_name + " неверно\n"; }
                                }
                                else { return "В ветке " + good_name + " неверные файлы\n"; }
                            }
                            else { return "В ветке" + good_name + " неверное кол-во файлов\n"; }
                        }
                        else { return "Наполнение файлов в ветке master неверно\n"; }
                    }
                    else { return "В ветке master неверные файлы\n"; }
                }
                else { return "В ветке master неверное кол-во файлов\n"; }
            }
            else { return "Неверное имя ветки\n"; }
        }
        else  { return "Неверное кол-во branches\n"; }
    }

    public String Check_Issues(int Good_issues,int Var_issues){
        if (Good_issues==Var_issues){
            driver.get(Var_Repository+"/issues");
            String Good_issues_str=pull_String("//a[@class='btn-link selected']",true)+pull_String("//a[@class='btn-link ']",true);
            Change_Tab(1);
            driver.get(Repository+"/issues");
            String Var_issues_str=pull_String("//a[@class='btn-link selected']",true)+pull_String("//a[@class='btn-link ']",true);
            Change_Tab(0);
            if (Good_issues_str.equals(Var_issues_str)){
                List<WebElement> Good_Issues_Open=driver.findElements(By.xpath("//div/div/div/div/div/div/div/div/div/a"));
                String[] Good_Issues_Str_Mas =new String[Good_Issues_Open.size()];
                for (int i=0;i<Good_Issues_Open.size();i++){
                    Good_Issues_Str_Mas[i]=Good_Issues_Open.get(i).getAttribute("textContent");
                }
                Change_Tab(1);
                List<WebElement> Var_Issues_Open=driver.findElements(By.xpath("//div/div/div/div/div/div/div/div/div/a"));
                String[] Var_Issues_Str_Mas =new String[Good_Issues_Open.size()];
                for (int i=0;i<Var_Issues_Open.size();i++){
                    Var_Issues_Str_Mas[i]=Var_Issues_Open.get(i).getAttribute("textContent");
                }
                Change_Tab(0);
                Arrays.sort(Var_Issues_Str_Mas);
                Arrays.sort(Good_Issues_Str_Mas);
                boolean ok=true;
                for (int i=0;i<Var_Issues_Open.size();i++){
                    if (!Var_Issues_Str_Mas[i].equals(Good_Issues_Str_Mas[i])){
                        ok=false;break;
                    }
                }
                if (ok){
                    driver.get(Var_Repository+"/issues?q=is%3Aissue+is%3Aclosed");
                    Good_issues_str=pull_String("//div[@class='flex-auto min-width-0 lh-condensed p-2 pr-3 pr-md-2']",true).toLowerCase();
                    for (String retval : Good_issues_str.split("#", 2)) {
                        Good_issues_str=retval;break;
                    }
                    Change_Tab(1);
                    driver.get(Repository+"/issues?q=is%3Aissue+is%3Aclosed");
                    Var_issues_str=pull_String("//div[@class='flex-auto min-width-0 lh-condensed p-2 pr-3 pr-md-2']",true).toLowerCase();
                    for (String retval : Var_issues_str.split("#", 2)) {
                        Var_issues_str=retval;break;
                    }
                    Change_Tab(0);
                    if (Good_issues_str.equals(Var_issues_str)){
                        return "";
                    }
                    else { return "Имя закрытого issues неверно\n"; }
                }
                else { return "Неверное имя открытого issue/issues\n"; }
            }
            else {return "Ошибка в issues. Должно быть 2 открытых, 1 закрытый\n"; }
        }
        else  { return "Не совпадает кол-во issues\n"; }
    }

    public String Check_PullRequests(int Good_pull,int Var_pull){
        if (Good_pull==Var_pull){
            driver.get(Var_Repository+"/pulls");
            String Good_pull_str=pull_String("//a[@class='btn-link selected']",true)+pull_String("//a[@class='btn-link ']",true);
            Change_Tab(1);
            driver.get(Repository+"/pulls");
            String Var_pull_str=pull_String("//a[@class='btn-link selected']",true)+pull_String("//a[@class='btn-link ']",true);
            Change_Tab(0);
            if (Good_pull_str.equals(Var_pull_str)){
                Good_pull_str=pull_String("//div[@class='flex-auto min-width-0 lh-condensed p-2 pr-3 pr-md-2']",true).toLowerCase();
                for (String retval : Good_pull_str.split("#", 2)) {
                    Good_pull_str=retval; break;
                }
                Change_Tab(1);
                Var_pull_str=pull_String("//div[@class='flex-auto min-width-0 lh-condensed p-2 pr-3 pr-md-2']",true).toLowerCase();
                for (String retval : Var_pull_str.split("#", 2)) {
                    Var_pull_str=retval; break;
                }
                Change_Tab(0);
                if (Good_pull_str.equals(Var_pull_str)){
                    driver.get(Var_Repository+"/pulls?q=is%3Apr+is%3Aclosed");
                    Good_pull_str=pull_String("//div[@class='flex-auto min-width-0 lh-condensed p-2 pr-3 pr-md-2']",true).toLowerCase();
                    for (String retval : Good_pull_str.split("#", 2)) {
                        Good_pull_str=retval; break;
                    }
                    Change_Tab(1);
                    driver.get(Repository+"/pulls?q=is%3Apr+is%3Aclosed");
                    Var_pull_str=pull_String("//div[@class='flex-auto min-width-0 lh-condensed p-2 pr-3 pr-md-2']",true).toLowerCase();
                    for (String retval : Var_pull_str.split("#", 2)) {
                        Var_pull_str=retval;break;
                    }
                    Change_Tab(0);
                    if (Good_pull_str.equals(Var_pull_str)){
                        return "";
                    }
                    else { return "Имя закрытого pull_request неверно,либо не назначен label\n"; }
                }
                else { return "Имя открытого pull_request неверно,либо не назначен label\n"; }
            }
            else {return "Ошибка в pull_requests. Должно быть 1 открытый, 1 закрытый\n"; }
        }
        else {return "Кол-во pull_request неверно\n";}
    }

    public String Check_Wiki(){
        String str="";
        driver.get(Var_Repository + "/wiki");
        if (driver.findElements(By.xpath("//div[@class='markdown-body']/p[1]")).size() != 0) {
            String Var_Wiki = pull_String("//li[2]/strong[1]/a[@class='d-block' and 1]",true);
            String Var_String = pull_String("//div[@class='markdown-body']/p[1]",false);
            Change_Tab(1);
            driver.get(Repository + "/wiki");
            String Good_Wiki = pull_String("//li[2]/strong[1]/a[@class='d-block' and 1]",true);
            String Good_String = pull_String("//div[@class='markdown-body']/p[1]",false);
            Change_Tab(0);
            if(!Var_String.equals(Good_String)){
                str+="Надпись на странице Home: '"+Var_String+"'\nа должно быть: '"+Good_String+"'\n";}
            if(Good_Wiki.equals(Var_Wiki)) {
                driver.get(Var_Repository + "/wiki/" + Var_Wiki);
                Var_String = pull_String("//div[@class='markdown-body']/p[1]",false);
                Change_Tab(1);
                driver.get(Repository + "/wiki/" + Good_Wiki);
                Good_String = pull_String("//div[@class='markdown-body']/p[1]",false);
                Change_Tab(0);
                if(!Good_String.equals(Var_String))
                { str+="Надпись на странице варианта: '"+Var_String+"'\nа должно быть: '"+Good_String+"'\n"; }
            } else { str += "Вторая страница Wiki названа неверно\n";}
        } else { str += "Wiki не заполнена вообще.\n"; }
        return str;
    }

    public String Check_Project(int Good_project,int Var_project){
        driver.get(Var_Repository + "/projects/");
        String Var_Name=driver.findElement(By.xpath("//a[@class='link-gray-dark mr-1']")).getAttribute("textContent");
        Change_Tab(1);
        driver.get(Repository + "/projects/");
        String Rep_Name=driver.findElement(By.xpath("//a[@class='link-gray-dark mr-1']")).getAttribute("textContent");
        Change_Tab(0);
        if (Var_Name.equals(Rep_Name)) {
            String str = "";
            String Good_issue, Var_issue;
            if (Var_project == Good_project) {
                driver.get(Var_Repository + "/projects/1");
                Change_Tab(1);
                driver.get(Repository + "/projects/1");
                String count_path = "div[@class='clearfix js-details-container details-container Details js-add-note-container' and 1]/div[@class='hide-sm position-relative p-sm-2' and 1]/span[1]";
                String name_path = "div[@class='clearfix js-details-container details-container Details js-add-note-container' and 1]/div[@class='hide-sm position-relative p-sm-2' and 1]/h3[1]/span[@class='js-project-column-name' and 1]";
                if (driver.findElements(By.xpath("//div[1]/div[1]/div/span")).size() != 0) {
                    if (pull_INT("//div[1]/" + count_path) >= 1) {
                        Var_issue = pull_String("//div[1]/div/article[1]/div/div/div/a", false);
                        Change_Tab(0);
                        Good_issue = pull_String("//div[1]/div/article[1]/div/div/div/a", false);
                        if (!Good_issue.equals(Var_issue)) {
                            str += "Доска " + pull_String("//div[1]/" + name_path, false) + " не содержит задачи: " + Good_issue + "\n";
                        }
                    } else {
                        str += "Доска " + pull_String("//div[1]/" + name_path, false) + " не содержит задач.\n";
                    }
                } else {
                    str += "Отсутствует 1-я доска.\n";
                }

                if (driver.findElements(By.xpath("//div[2]/div[1]/div/span")).size() != 0) {
                    if (pull_INT("//div[2]/" + count_path) >= 1) {
                        Change_Tab(1);
                        Var_issue = pull_String("//div[2]/div/article[1]/div/div/div/a", false);
                        Change_Tab(0);
                        Good_issue = pull_String("//div[2]/div/article[1]/div/div/div/a", false);
                        if (!Good_issue.equals(Var_issue)) {
                            str += "Доска " + pull_String("//div[2]/" + name_path, false) + " не содержит задачи: " + Good_issue + "\n";
                        }
                    } else {
                        str += "Доска " + pull_String("//div[2]/" + name_path, false) + " не содержит задач.\n";
                    }
                } else {
                    str += "Отсутствует 2-я доска.\n";
                }

                if (driver.findElements(By.xpath("//div[3]/div[1]/div/span")).size() != 0) {
                    if (pull_INT("//div[3]/" + count_path) >= 1) {
                        Change_Tab(1);
                        Var_issue = pull_String("//div[3]/div/article[1]/div/div/div/a", false);
                        Change_Tab(0);
                        Good_issue = pull_String("//div[3]/div/article[1]/div/div/div/a", false);
                        if (!Good_issue.equals(Var_issue)) {
                            str += "Доска " + pull_String("//div[3]/" + name_path, false) + " не содержит задачи: " + Good_issue + "\n";
                        }
                    } else {
                        str += "Доска " + pull_String("//div[3]/" + name_path, false) + " не содержит задач.\n";
                    }
                } else {
                    str += "Отсутствует 3-я доска.\n";
                }
            } else {
                str += "Отсутсвует project, либо он закрыт.\n";
            }
            return str;
        }
        return "Неверное имя project\n";
    }

    public String Check_Labels(){
        Change_Tab(0);
        driver.get(Var_Repository+"/labels");
        int Good_Labels=pull_INT("//span[@class='js-labels-count']");
        Change_Tab(1);
        driver.get(Repository+"/labels");
        int Var_Labels=pull_INT("//span[@class='js-labels-count']");
        Change_Tab(0);
        if (Good_Labels==Var_Labels){
            String Good_Labels_Name=pull_String("//div[10]/div[@class='col-3 pr-3' and 1]/a[@class='IssueLabel--big d-inline-block v-align-top lh-condensed js-label-link' and 1]/span[1]",true);
            Change_Tab(1);
            String Var_Labels_Name=pull_String("//div[10]/div[@class='col-3 pr-3' and 1]/a[@class='IssueLabel--big d-inline-block v-align-top lh-condensed js-label-link' and 1]/span[1]",true);
            Change_Tab(0);
            if (Good_Labels_Name.equals(Var_Labels_Name)){
                Good_Labels_Name=pull_String("//a[@class='muted-link']",true);
                Change_Tab(1);
                if (driver.findElements(By.xpath("//a[@class='muted-link']")).size()!=0) {
                    Var_Labels_Name = pull_String("//a[@class='muted-link']", true);
                }
                else {  Change_Tab(0); return "Label не назначен на задачи или или/и pull_requests \n";}
                Change_Tab(0);
                if (Good_Labels_Name.equals(Var_Labels_Name)){
                    return "";
                }
                else { return "Label верен, но назначен не на все задачи или/и pull_requests\n"; }
            }
            else { return "Имя labels не совпадает\n"; }
        }
        else { return "Кол-во labels не совпадает\n"; }
    }


    public String Check_Milestone(){
        driver.get(Var_Repository+"/milestones");
        String Good_Milestone=pull_String("//a[@class='btn-link selected']",true)+pull_String("//a[@class='btn-link ']",true);
        Change_Tab(1);
        driver.get(Repository+"/milestones");
        String Var_Milestone=pull_String("//a[@class='btn-link selected']",true)+pull_String("//a[@class='btn-link ']",true);
        Change_Tab(0);
        if (Good_Milestone.equals(Var_Milestone)){
            driver.findElement(By.xpath("//h2/a[1]")).click();
            Good_Milestone=pull_String("//h2",true);
            Change_Tab(1);
            driver.findElement(By.xpath("//h2/a[1]")).click();
            Var_Milestone=pull_String("//h2",true);
            Change_Tab(0);
            if (Good_Milestone.equals(Var_Milestone)){
                Good_Milestone=pull_String("//a[@class='btn-link selected']",true)+pull_String("//a[@class='btn-link ']",true);
                Change_Tab(1);
                Var_Milestone=pull_String("//a[@class='btn-link selected']",true)+pull_String("//a[@class='btn-link ']",true);
                Change_Tab(0);
                if(Good_Milestone.equals(Var_Milestone)){
                    return "";
                }
                else { return "В milestone должно быть 5 задач(3 открытых, 2 закрытых)\n"; }
            }
            else  {return "Имя milestone некорректно\n"; }
        }
        else {return "Отсутствует либо закрыт milestone\n"; }
    }

    public String Check_Readme(){
        String Readme_Good = pull_String("//article",true);
        Change_Tab(1);
        if (driver.findElements(By.xpath("//article")).size()!=0) {
            String Readme_Var = pull_String("//article", true);
            Change_Tab(0);
            if (Readme_Good.equals(Readme_Var)) { return ""; }
            else { return "Файл Readme неверен\n"; }
        } else { return "Файл Readme не найден\n"; }
    }

    private String pull_String(String tmp, boolean DeleteSpaces){
        if (DeleteSpaces) return driver.findElement(By.xpath(tmp)).getAttribute("textContent").replaceAll(" ","").replaceAll("\n","");
        else return driver.findElement(By.xpath(tmp)).getAttribute("textContent");
    }

    private int pull_INT(String tmp){
        return Integer.parseInt(driver.findElement(By.xpath(tmp)).getAttribute("textContent").replaceAll(" ","").replaceAll("\n",""));
    }

    public void Change_Tab(int tab){
        ArrayList<String> tabs = new ArrayList<String>(driver.getWindowHandles());
        driver.switchTo().window(tabs.get(tab));
    }

    public void Add_Tab(){
        ((JavascriptExecutor)driver).executeScript("window.open()");
        ArrayList<String> tabs = new ArrayList<String>(driver.getWindowHandles());
        driver.switchTo().window(tabs.get(1));
        driver.get(Repository);
        if (driver.findElements(By.xpath("//div[@class='blankslate blankslate-narrow']")).size()!=0){
            empty=true;
        }
    }

    public void test() {
        if (Var_Repository != null) {
            if (!empty){
                final int Good_branches = pull_INT("//li[2]/a[1]/span[@class='num text-emphasized' and 1]");
                final int Good_issues = pull_INT("//span[2]/a[@class='js-selected-navigation-item reponav-item' and 1]/span[@class='Counter' and 2]");
                final int Good_pull_request = pull_INT("//*[1]/span[@class='Counter' and 2]");
                final int Good_projects = pull_INT("//nav/a[@class='js-selected-navigation-item reponav-item' and 1]/span[@class='Counter' and 1]");
                Change_Tab(1);
                final int Var_branches = pull_INT("//li[2]/a[1]/span[@class='num text-emphasized' and 1]");
                final int Var_issues = pull_INT("//span[2]/a[@class='js-selected-navigation-item reponav-item' and 1]/span[@class='Counter' and 2]");
                final int Var_pull_request = pull_INT("//*[1]/span[@class='Counter' and 2]");
                final int Var_projects = pull_INT("//nav/a[@class='js-selected-navigation-item reponav-item' and 1]/span[@class='Counter' and 1]");
                Change_Tab(0);

                result += Check_Readme(); //Done
                result += Check_Labels(); //Done
                result += Check_Milestone(); //Done
                result += Check_Project(Good_projects,Var_projects); //Реализовать проверку проекта In progress
                result += Check_PullRequests(Good_pull_request,Var_pull_request); //Done
                result += Check_Issues(Good_issues,Var_issues); //Done
                result += Check_Branches(Good_branches,Var_branches); //Done
                result += Check_Wiki(); //In progress

                if ("".equals(result)) {itog_ozenka = "1";}
            } else { result="Репозиторий пуст\n";
            }
        } else {System.out.println("Не найден вариант в файле\n");
        }
        driver.quit();
    }
}