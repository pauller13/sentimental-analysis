# %%
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

# %%
def create_driver():
    options = webdriver.ChromeOptions()

    options.page_load_strategy = 'eager'  # ne pas attendre le chargement complet (pubs, trackers...)

    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--blink-settings=imagesEnabled=false")  # accélère le chargement
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless=new")  # décommente si besoin

    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(25)
    driver.set_script_timeout(10)

    return driver

# %%
def is_driver_alive(driver):
    try:
        driver.set_page_load_timeout(5)
        _ = driver.current_url
        driver.set_page_load_timeout(25)  # on remet le timeout normal après le check
        return True
    except Exception:
        return False

# %%
driver = create_driver()

# %%
from selenium.common.exceptions import (
    TimeoutException, WebDriverException, InvalidSessionIdException
)
from urllib3.exceptions import ReadTimeoutError
import time

def safe_get(url, max_retries=3):
    global driver
    for attempt in range(max_retries):

        if not is_driver_alive(driver):
            print("⚠️ Driver mort, recréation...")
            try:
                driver.quit()
            except Exception:
                pass
            driver = create_driver()

        try:
            driver.get(url)
            time.sleep(3)
            return True

        except TimeoutException as e:
            msg = str(e)
            print(f"Timeout sur {url}, tentative {attempt+1}/{max_retries} : {msg[:100]}")

            if "receiving message from renderer" in msg:
                print("Renderer bloqué -> recréation immédiate du driver")
                try:
                    driver.quit()
                except Exception:
                    pass
                driver = create_driver()
            else:
                try:
                    driver.execute_script("window.stop();")
                except Exception:
                    try:
                        driver.quit()
                    except Exception:
                        pass
                    driver = create_driver()

        except (WebDriverException, InvalidSessionIdException, ReadTimeoutError) as e:
            print(f"Erreur driver sur {url} (tentative {attempt+1}) : {e}")
            try:
                driver.quit()
            except Exception:
                pass
            driver = create_driver()

    return False

# %%
reviews_data = []

# %%
def get_label(stars):
    stars = int(stars)

    if stars >= 4:
        return "pos"
    elif stars <= 2:
        return "neg"
    else:
        return "neutre"

# %%
# # 1. récupérer toutes les catégories
# categories_url = "https://fr.trustpilot.com/categories"


# driver.get(categories_url)
# time.sleep(3)

# categories = driver.find_elements(By.CLASS_NAME, "styles_container__ptvcf")

# categories_urls = []

# for category in categories:

#     elements = category.find_elements(By.TAG_NAME, "li")

#     for element in elements:

#         try:
#             href = element.find_element(By.TAG_NAME, "a").get_attribute("href")

#             if href not in categories_urls:
#                 categories_urls.append(href)

#         except:
#             continue

# print(f"{len(categories_urls)} catégories trouvées")

# %%
# # 2. récupérer les entreprises
# enterprise_urls = []

# driver = create_driver()

# pages_scraped = 0
# RECYCLE_EVERY = 100

# for category_url in categories_urls:

#     print(f"Scraping categorie : {category_url}")

#     current_url = category_url

#     while current_url:

#         if not safe_get(current_url):
#             print(f"Impossible de charger {current_url} après plusieurs tentatives, passage à la suite.")
#             break

#         try:
#             cards = driver.find_elements(
#                 By.CLASS_NAME,
#                 "CDS_Card_card__146e7a"
#             )

#             for card in cards:

#                 try:
#                     businesses = card.find_elements(
#                         By.CLASS_NAME,
#                         "styles_businessUnitMain__wRgqU"
#                     )

#                     for business in businesses:

#                         try:
#                             span = business.find_element(
#                                 By.CSS_SELECTOR,
#                                 'span[role="button"]'
#                             )

#                             review_count = span.text.split(" ")[0]
#                             count = int(
#                                 review_count
#                                 .replace(" ", "")
#                                 .replace("\u202f", "")
#                             )

#                             if count > 3:
#                                 href = card.find_element(
#                                     By.TAG_NAME,
#                                     "a"
#                                 ).get_attribute("href")

#                                 if href not in enterprise_urls:
#                                     enterprise_urls.append(href)

#                         except Exception:
#                             continue

#                 except Exception:
#                     continue

#             print(f"{len(enterprise_urls)} entreprises")

#             pages_scraped += 1
#             if pages_scraped % RECYCLE_EVERY == 0:
#                 print("♻️ Recyclage préventif du driver")
#                 try:
#                     driver.quit()
#                 except Exception:
#                     pass
#                 driver = create_driver()

#             # Pagination
#             try:
#                 pagination = driver.find_element(
#                     By.CSS_SELECTOR,
#                     '[name="pagination-button-next"]'
#                 )

#                 next_url = pagination.get_attribute("href")

#                 if next_url:
#                     current_url = next_url
#                 else:
#                     current_url = None

#             except Exception:
#                 current_url = None

#         except Exception as e:
#             print(f"Erreur sur {current_url} : {e}")

#             try:
#                 pagination = driver.find_element(
#                     By.CSS_SELECTOR,
#                     '[name="pagination-button-next"]'
#                 )
#                 current_url = pagination.get_attribute("href")
#             except Exception:
#                 current_url = None

# print(f"Total entreprises : {len(enterprise_urls)}")

# %%
# len(enterprise_urls)

# %%
company_path="../data/trustpilot_urls.csv"
df = pd.read_csv(company_path)
df['url'].to_list()

# %%
#3-scraper les commentaires
import os


# Fichier de sortie
reviews_csv = "../data/reviews.csv"
MAX_PAGE = 10

# Parcours des entreprises
for index, row in df.iterrows():

    site_url = row["url"]

    print(f"\n{'=' * 60}")
    print(f"Entreprise : {site_url}")
    print(f"{'=' * 60}")

    # IMPORTANT : réinitialiser pour chaque entreprise
    page = 1

    current_url = site_url
    company_reviews = []
    processed = False

    while page <= MAX_PAGE:

        print(f"Page {page}/{MAX_PAGE} : {current_url}")

        if not safe_get(current_url):
            print(
                f"Impossible de charger {current_url} après plusieurs tentatives."
            )
            break

        try:
            time.sleep(8)

            main_content = driver.find_element(
                By.CLASS_NAME,
                "styles_mainContent__d9oos"
            )

            articles = main_content.find_elements(
                By.TAG_NAME,
                "article"
            )

            print(f"{len(articles)} articles trouvés")

            # =====================================================
            # SCRAPING DES REVIEWS
            # =====================================================
            for article in articles:

                # -------------------------
                # Contenu de la review
                # -------------------------
                try:
                    try:
                        element = article.find_element(
                            By.TAG_NAME,
                            "p"
                        )
                    except:
                        element = article.find_element(
                            By.TAG_NAME,
                            "h2"
                        )

                    content = element.text.strip()

                    if len(content) < 3:
                        continue

                except:
                    continue

                # -------------------------
                # Étoiles
                # -------------------------
                try:
                    stars = article.find_element(
                        By.CLASS_NAME,
                        "styles_reviewHeader__DzoAZ"
                    ).get_attribute(
                        "data-service-review-rating"
                    )

                    label = get_label(stars)

                except:
                    continue

                review = {
                    "content": content,
                    "label": label,
                    "type": "commentaire",
                    "source": site_url
                }

                company_reviews.append(review)

                # Si tu veux conserver reviews_data
                reviews_data.append(review)

            # =====================================================
            # LIMITE DES 10 PAGES
            # =====================================================
            if page >= MAX_PAGE:
                print(f"Limite de {MAX_PAGE} pages atteinte.")
                processed = True
                break

            # =====================================================
            # PAGINATION
            # =====================================================
            try:
                pagination = main_content.find_element(
                    By.CSS_SELECTOR,
                    '[name="pagination-button-next"]'
                )

                next_url = pagination.get_attribute("href")

                if not next_url:
                    print("Pas de page suivante.")
                    processed = True
                    break

                current_url = next_url
                page += 1

            except Exception:
                print("Pas de page suivante.")
                processed = True
                break

        except Exception as e:

            print(f"Erreur sur {current_url}: {e}")
            break

    # =====================================================
    # ENTREPRISE TRAITÉE
    # =====================================================
    if processed:

        print(
            f"Scraping terminé : {len(company_reviews)} reviews trouvées."
        )

        # =====================================================
        # SAUVEGARDE DES REVIEWS DANS LE CSV
        # =====================================================
        if company_reviews:

            reviews_df = pd.DataFrame(company_reviews)

            if os.path.exists(reviews_csv):

                reviews_df.to_csv(
                    reviews_csv,
                    mode="a",
                    header=False,
                    index=False,
                    encoding="utf-8-sig"
                )

            else:

                reviews_df.to_csv(
                    reviews_csv,
                    mode="w",
                    header=True,
                    index=False,
                    encoding="utf-8-sig"
                )

            print(
                f"{len(company_reviews)} reviews ajoutées à "
                f"{reviews_csv}"
            )

        # =====================================================
        # SUPPRESSION DE L'ENTREPRISE DU DATAFRAME
        # =====================================================
        df.drop(index=index, inplace=True)

        df.to_csv(
            company_path,
            index=False,
            encoding="utf-8-sig"
        )

        print(f"URL supprimée du DataFrame : {site_url}")

    else:

        print(
            f"URL NON supprimée car le scraping n'a pas été terminé : "
            f"{site_url}"
        )


# %%
driver.quit()


# %%
df = pd.DataFrame(reviews_data)
df.info

# %%
df = pd.read_csv("../data/trustpilot_reviews.csv")


# %%
# df =  pd.read_csv("../data/trustpilot_reviews.csv")


# %%
# df.dropna(inplace=True)

# %%
# df.head()

# %%
# df.replace('\n', ' ', regex=True, inplace=True)
# df.replace('\r', ' ', regex=True, inplace=True)

# %%
# df.info()

# %%
# df.sample(10)

# %%
# df[df["label"] == "neg"].shape

# %%
# df[df["label"] == "pos"].shape

# %%
# df.drop_duplicates(inplace=True)
# df.drop(df[df['label'] == 'neutre'].index, inplace=True)

# %%
# from sklearn.utils import shuffle

# %%
# pos_df = df[df["label"] == "pos"]
# neg_df = df[df["label"] == "neg"]
# neu_df= df[df["label"] == "neutre"]

# %%
# pos_df =shuffle(pos_df)
# pos_df.reset_index(inplace=True, drop=True)
# pos_df

# %%
# neg_df =shuffle(neg_df)
# neg_df.reset_index(inplace=True, drop=True)
# neg_df

# %%
# neg_df = neg_df[:len(neu_df)]
# pos_df = pos_df[:len(neg_df)]

# %%
# neg_df.shape, pos_df.shape

# %%
# df = pd.concat([neg_df, pos_df], axis=0)

# %%
# df.head()

# %%
# df.drop(columns=["source"], inplace=True)

# %%
# df["content"] = df["content"].apply(lambda x: x.lower())

# %%
# df = shuffle(df)
# df.reset_index(inplace=True, drop=True)
# df.to_csv("data/sentiment_data.csv", index=False, encoding="utf-8-sig")

# %%
# df.sample(frac=0.1, random_state=42)

# %%
# import emoji

# %%
# df['content'].apply(
#     lambda x: any(char in emoji.EMOJI_DATA for char in str(x))
# ).sum()

# %%
# df['content_without_emojis'] = df['content'].apply(
#         lambda x: emoji.demojize(str(x), language='fr')
#     )


# %%
# df['content_without_emojis'].apply(
#     lambda x: any(char in emoji.EMOJI_DATA for char in str(x))
# ).sum()

# %%
# df.head()

# %%
# import spacy
# nlp = spacy.load("fr_core_news_sm")
# import string

# %%
# string.punctuation

# %%
# df["content_without_emojis"].apply(lambda x: " ".join([char for char in x if char not in string.punctuation]))

# %%

# def preprocess_text(text):
#     text = "".join([char for char in text if char not in string.punctuation])
#     doc = nlp(text)    
#     return [
#         token.lemma_
#         for token in doc
#         if not token.is_punct
#         and not token.is_stop
#         and not token.is_space
#     ]

# %%
# df['content_preprocessed'] = df['content_without_emojis'].apply(preprocess_text)
# df.head()

# %%
# df.to_csv("sentiment_data.csv", index=False, encoding="utf-8-sig")

# %%
# df['label'].value_counts()


