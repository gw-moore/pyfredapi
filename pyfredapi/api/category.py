"""This module contains the FredCategory implementation."""


from typing import Literal, Optional, Union

from pydantic import BaseModel, Extra, PositiveInt

from .base import RETURN_FORMAT, FredBase, Json, JsonOrPandas, ReturnFormat
from .utils import _convert_to_pandas


class CategoryApiParameters(BaseModel):
    """Represents the parameters accepted by the FRED Category endpoints."""

    category_id: Optional[int] = None
    realtime_start: Optional[str] = None
    realtime_end: Optional[str] = None
    limit: Optional[int] = None
    offset: Optional[PositiveInt] = None
    order_by: Optional[
        Literal[
            "series_id",
            "title",
            "units",
            "frequency",
            "seasonal_adjustment",
            "realtime_start",
            "realtime_end",
            "last_updated",
            "observation_start",
            "observation_end",
            "popularity",
            "group_popularity",
        ]
    ] = None
    sort_order: Optional[Literal["acs", "desc"]] = None
    filter_variable: Optional[
        Literal["frequency", "units", "seasonal_adjustment"]
    ] = None
    filter_value: Optional[str] = None
    tag_names: Optional[str] = None
    exclude_tag_names: Optional[str] = None

    class Config:
        extra = Extra.allow


class FredCategory(FredBase):
    """Represents a FRED Category."""

    def get_category(self, category_id: Optional[int] = None, **kwargs) -> Json:
        """Get category by ID. https://fred.stlouisfed.org/docs/api/fred/category.html.

        Parameters
        ----------
        category_id : str | None
            Category id of interest.
        **kwargs : dict, optional
            Additional parameters to FRED API category/ endpoint. Refer to the FRED documentation for a list of all possible parameters.

        Returns
        -------
        Dictionary representing the json response.
        """
        params = CategoryApiParameters(category_id=category_id, **kwargs)
        return self._get(
            endpoint="category",
            params=params.dict(exclude_none=True),
        )

    def get_category_children(
        self, category_id: Optional[int] = None, **kwargs
    ) -> Json:
        """Get category children by category ID. https://fred.stlouisfed.org/docs/api/fred/category_children.html.

        Parameters
        ----------
        category_id : str | None
            Category id of interest.
        **kwargs : dict, optional
            Additional parameters to FRED API category/children endpoint. Refer to the FRED documentation for a list of all possible parameters.

        Returns
        -------
        Dictionary representing the json response.
        """
        params = CategoryApiParameters(category_id=category_id, **kwargs)
        return self._get(
            endpoint="category/children",
            params=params.dict(exclude_none=True),
        )

    def get_category_related(self, category_id: int, **kwargs) -> Json:
        """Get related categories by category ID. https://fred.stlouisfed.org/docs/api/fred/category_related.html.

        Parameters
        ----------
        category_id : str
            Category id of interest.
        **kwargs : dict, optional
            Additional parameters to FRED API category/children endpoint. Refer to the FRED documentation for a list of all possible parameters.


        Returns
        -------
        Dictionary representing the json response.
        """
        params = CategoryApiParameters(category_id=category_id, **kwargs)
        return self._get(
            endpoint="category/related",
            params=params.dict(exclude_none=True),
        )

    def get_category_series(
        self,
        category_id: int,
        return_format: Union[RETURN_FORMAT, ReturnFormat] = "json",
        **kwargs,
    ) -> JsonOrPandas:
        """Get the series in a category by category ID. https://fred.stlouisfed.org/docs/api/fred/category_series.html.

        Parameters
        ----------
        category_id : str
            Category id of interest.
        return_format : str | ReturnFormat
            Define how to return the response. Must be either 'json' or 'pandas'.

        Returns
        -------
        Either a dictionary representing the json response or a pandas dataframe.
        """
        return_format = ReturnFormat(return_format)

        params = CategoryApiParameters(category_id=category_id, **kwargs)
        response = self._get(
            endpoint="category/series",
            params=params.dict(exclude_none=True),
        )

        if return_format == ReturnFormat.pandas:
            return _convert_to_pandas(response["seriess"])
        return response

    def get_category_tags(
        self,
        category_id: Optional[int] = None,
        return_format: Union[RETURN_FORMAT, ReturnFormat] = "json",
        **kwargs,
    ) -> JsonOrPandas:
        """Get the FRED tags for a category by category ID. https://fred.stlouisfed.org/docs/api/fred/category_tags.html.

        Parameters
        ----------
        category_id : str | None
            Category id of interest.
        return_format : str | ReturnFormat
            Define how to return the response. Must be either 'json' or 'pandas'.

        Returns
        -------
        Either a dictionary representing the json response or a pandas dataframe.
        """
        return_format = ReturnFormat(return_format)

        params = CategoryApiParameters(category_id=category_id, **kwargs)
        response = self._get(
            endpoint="category/tags",
            params=params.dict(exclude_none=True),
        )

        if return_format == ReturnFormat.pandas:
            return _convert_to_pandas(response["tags"])
        return response

    def get_category_related_tags(
        self,
        category_id: Optional[int] = None,
        return_format: Union[RETURN_FORMAT, ReturnFormat] = "json",
        **kwargs,
    ) -> JsonOrPandas:
        """Get the related FRED tags for a category by category ID. https://fred.stlouisfed.org/docs/api/fred/category_related_tags.html.

        Parameters
        ----------
        category_id : str | None
            Category id of interest.
        return_format : str | ReturnFormat
            Define how to return the response. Must be either 'json' or 'pandas'.

        Returns
        -------
        Either a dictionary representing the json response or a pandas dataframe.
        """
        return_format = ReturnFormat(return_format)

        params = CategoryApiParameters(category_id=category_id, **kwargs)
        response = self._get(
            endpoint="category/related_tags",
            params=params.dict(exclude_none=True),
        )

        if return_format == ReturnFormat.pandas:
            return _convert_to_pandas(response["tags"])
        return response
