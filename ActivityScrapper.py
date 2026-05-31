from pydantic import BaseModel, Field
from typing import Optional

class Activity(BaseModel):
    title: str = Field(description="The title of the activity.")
    rating: float = Field(description="The average user rating out of 10.")
    reviews_count: int = Field(description="The total number of reviews received.")
    travelers_count: Optional[int] = Field(description="The number of travelers who have participated.")
    cancellation_policy: Optional[str] = Field(description="The cancellation policy for the activity.")
    description: str = Field(description="A detailed description of what the activity entails.")
    duration: str = Field(description="The duration of the activity, usually given in hours or days.")
    language: Optional[str] = Field(description="The primary language in which the activity is conducted.")
    category: str = Field(description="The category of the activity, such as 'Boat Trip', 'City Tours', etc.")
    price: float = Field(description="The price of the activity.")
    currency: str = Field(description="The currency in which the price is denominated, such as USD, EUR, GBP, etc.")

    
class ActivityScrapper(BaseModel):
    Activities: list[Activity] = Field("List of all the activities listed in the text")