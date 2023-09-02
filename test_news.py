from news import (
    get_articles_by_category,
    get_articles_by_query,
    get_sources_by_country,
    NewsAPIClient,
)
import pytest

null = ""  # null is not defined in Python, so we define it as an empty string for the tests


# Mock the NewsAPIClient class
@pytest.fixture
def mock_api_client(mocker):
    # Create a mock object for the NewsAPIClient class
    return mocker.Mock(spec=NewsAPIClient)


def test_get_articles_by_category(mock_api_client):
    """Test get_articles_by_category."""
    # Mock the API client's get_articles method
    mock_api_client.get_articles.return_value = [
        {
            "source": {"id": "usa-today", "name": "USA Today"},
            "author": ", USA TODAY",
            "title": "FIFA president Infantino: World Cup kiss shouldn't have happened - USA TODAY",
            "description": "Eleven days after Luis Rubiales sparked international backlash during Spains' World Cup win, FIFA president Gianni Infantino broke his silence.",
            "url": "https://www.usatoday.com/story/sports/soccer/worldcup/2023/08/31/fifa-president-infantino-world-cup-kiss-should-not-happen/70732592007/",
            "urlToImage": "https://www.gannett-cdn.com/authoring/authoring-images/2023/07/19/USAT/70428923007-AFP%201541238530.JPG?auto=webp&crop=5499,3108,x0,y279&format=pjpg&width=1200",
            "publishedAt": "2023-09-01T00:40:05Z",
            "content": "Eleven days after Royal Spanish Football Federation president Luis Rubiales sparked international backlash during the country's World Cup celebrations, FIFA president Gianni Infantino is breaking his\u2026 [+3017 chars]",
        },
        {
            "source": {"id": "cbs-news", "name": "CBS News"},
            "author": "Ben Warwick",
            "title": "Romi Bean sits down with Coach Prime for Coach Prime's Playbook ahead of the season opener against TCU - CBS News",
            "description": 'Romi Bean chats with Deion Sanders, head coach of the CU Buffs football team, on "Coach Prime\'s Playbook."',
            "url": "https://www.cbsnews.com/colorado/news/romi-bean-sits-down-with-coach-prime-for-coach-primes-playbook-ahead-of-the-season-opener-against-tcu/",
            "urlToImage": "https://assets1.cbsnewsstatic.com/hub/i/r/2023/08/30/9a41299e-2905-489b-9ccc-2302febea714/thumbnail/1200x630/eea79be3124e63c8c50bc286dc7c3e3b/prime3.jpg?v=bd30f47a894d621fb3691fc64d1442e9",
            "publishedAt": "2023-09-01T00:30:09Z",
            "content": 'The CU Buffaloes will take the field for the first time in the 2023 season this Saturday at 10:00 a.m. against the TCU Horned Frogs.\u00a0\r\nRomi Bean sat down with new head coach, Deion Sanders, on "Coach\u2026 [+6646 chars]',
        },
    ]

    # Call the function being tested
    result = get_articles_by_category("business", mock_api_client)

    # Assert the expected behavior
    assert len(result) == 2
    assert (
        result[0]["title"]
        == "FIFA president Infantino: World Cup kiss shouldn't have happened - USA TODAY"
    )
    assert result[1]["author"] == "Ben Warwick"


def test_get_sources_by_country(mock_api_client):
    """Test get_sources_by_country."""
    mock_api_client.get_sources.return_value = [
        {
            "id": "ars-technica",
            "name": "Ars Technica",
            "description": "The PC enthusiast's resource. Power users and the tools they love, without computing religion.",
            "url": "http://arstechnica.com",
            "category": "technology",
            "language": "en",
            "country": "us",
        },
        {
            "id": "associated-press",
            "name": "Associated Press",
            "description": "The AP delivers in-depth coverage on the international, politics, lifestyle, business, and entertainment news.",
            "url": "https://apnews.com/",
            "category": "general",
            "language": "en",
            "country": "us",
        },
    ]

    # Call the function being tested
    result = get_sources_by_country("us", mock_api_client)

    assert len(result) == 2
    assert result[0]["name"] == "Ars Technica"
    assert result[1]["url"] == "https://apnews.com/"


def test_get_articals_by_query(mock_api_client):
    """Test get_articals_by_query."""
    mock_api_client.get_articles.return_value = [
        {
            "source": {"id": null, "name": "Mediapart"},
            "author": "Mathilde Goanec",
            "title": "L\u2019\u00e9cole selon Macron: ne manque plus que le lever de drapeau et l\u2019hymne national",
            "description": "Le pr\u00e9sident de la R\u00e9publique est d\u00e9cid\u00e9ment de la vieille \u00e9cole. Tout \u00e0 son projet de \u00ab\u00a0reciviliser\u00a0\u00bb une \u00ab\u00a0partie de la jeunesse\u00a0\u00bb, il veut faire de l\u2019\u00e9ducation son \u00ab\u00a0domaine r\u00e9serv\u00e9\u00a0\u00bb, en lui appliquant des recettes d\u00e9j\u00e0 dat\u00e9es.",
            "url": "https://www.mediapart.fr/journal/france/240823/l-ecole-selon-macron-ne-manque-plus-que-le-lever-de-drapeau-et-l-hymne-national",
            "urlToImage": "https://static.mediapart.fr/etmagine/og/journal/files/2023/08/24/20230824-img-macron-maitre-de-l-ecole-1.jpg",
            "publishedAt": "2023-08-24T16:11:03Z",
            "content": "Les cookies et technologies similaires que nous utilisons sur Mediapart sont de diff\u00e9rentes natures et nous permettent de poursuivre diff\u00e9rentes finalit\u00e9s. \r\nCertains sont n\u00e9cessaires au fonctionneme\u2026 [+1247 chars]",
        },
        {
            "source": {"id": null, "name": "Mediapart"},
            "author": "Floriane Louison",
            "title": "Un milliard d\u2019arbres: le bluff \u00e9colo de Macron pour sauver la for\u00eat",
            "description": "Un plan de renouvellement forestier est en cours d\u2019\u00e9laboration pour adapter la for\u00eat fran\u00e7aise au changement climatique. Il est orient\u00e9 autour d\u2019une annonce phare d\u2019Emmanuel Macron\u00a0: planter un milliard d\u2019arbres d\u2019ici \u00e0 dix\u00a0ans. Mais derri\u00e8re le coup de com\u2019 \u2026",
            "url": "https://www.mediapart.fr/journal/ecologie/070823/un-milliard-d-arbres-le-bluff-ecolo-de-macron-pour-sauver-la-foret",
            "urlToImage": "https://static.mediapart.fr/etmagine/og/journal/files/2023/08/04/024-4124110.jpg",
            "publishedAt": "2023-08-07T10:54:34Z",
            "content": "Les cookies et technologies similaires que nous utilisons sur Mediapart sont de diff\u00e9rentes natures et nous permettent de poursuivre diff\u00e9rentes finalit\u00e9s. \r\nCertains sont n\u00e9cessaires au fonctionneme\u2026 [+1247 chars]",
        },
    ]

    # Call the function being tested
    result = get_articles_by_query("Macron", "fr", mock_api_client)

    assert len(result) == 2
    assert result[0]["author"] == "Mathilde Goanec"
    assert result[1]["publishedAt"] == "2023-08-07T10:54:34Z"
