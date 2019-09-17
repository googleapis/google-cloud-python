# -*- coding: utf-8 -*-
import proto  # type: ignore


__protobuf__ = proto.module(package="google.cloud.vision.v1", manifest={"WebDetection"})


class WebDetection(proto.Message):
    r"""Relevant information for the image from the Internet.

    Attributes:
        web_entities (Sequence[~.web_detection.WebDetection.WebEntity]):
            Deduced entities from similar images on the
            Internet.
        full_matching_images (Sequence[~.web_detection.WebDetection.WebImage]):
            Fully matching images from the Internet.
            Can include resized copies of the query image.
        partial_matching_images (Sequence[~.web_detection.WebDetection.WebImage]):
            Partial matching images from the Internet.
            Those images are similar enough to share some
            key-point features. For example an original
            image will likely have partial matching for its
            crops.
        pages_with_matching_images (Sequence[~.web_detection.WebDetection.WebPage]):
            Web pages containing the matching images from
            the Internet.
        visually_similar_images (Sequence[~.web_detection.WebDetection.WebImage]):
            The visually similar image results.
        best_guess_labels (Sequence[~.web_detection.WebDetection.WebLabel]):
            The service's best guess as to the topic of
            the request image. Inferred from similar images
            on the open web.
    """

    class WebEntity(proto.Message):
        r"""Entity deduced from similar images on the Internet.

        Attributes:
            entity_id (str):
                Opaque entity ID.
            score (float):
                Overall relevancy score for the entity.
                Not normalized and not comparable across
                different image queries.
            description (str):
                Canonical description of the entity, in
                English.
        """
        entity_id = proto.Field(proto.STRING, number=1)
        score = proto.Field(proto.FLOAT, number=2)
        description = proto.Field(proto.STRING, number=3)

    class WebImage(proto.Message):
        r"""Metadata for online images.

        Attributes:
            url (str):
                The result image URL.
            score (float):
                (Deprecated) Overall relevancy score for the
                image.
        """
        url = proto.Field(proto.STRING, number=1)
        score = proto.Field(proto.FLOAT, number=2)

    class WebPage(proto.Message):
        r"""Metadata for web pages.

        Attributes:
            url (str):
                The result web page URL.
            score (float):
                (Deprecated) Overall relevancy score for the
                web page.
            page_title (str):
                Title for the web page, may contain HTML
                markups.
            full_matching_images (Sequence[~.web_detection.WebDetection.WebImage]):
                Fully matching images on the page.
                Can include resized copies of the query image.
            partial_matching_images (Sequence[~.web_detection.WebDetection.WebImage]):
                Partial matching images on the page.
                Those images are similar enough to share some
                key-point features. For example an original
                image will likely have partial matching for its
                crops.
        """
        url = proto.Field(proto.STRING, number=1)
        score = proto.Field(proto.FLOAT, number=2)
        page_title = proto.Field(proto.STRING, number=3)
        full_matching_images = proto.RepeatedField(
            proto.MESSAGE, number=4, message="WebDetection.WebImage"
        )
        partial_matching_images = proto.RepeatedField(
            proto.MESSAGE, number=5, message="WebDetection.WebImage"
        )

    class WebLabel(proto.Message):
        r"""Label to provide extra metadata for the web detection.

        Attributes:
            label (str):
                Label for extra metadata.
            language_code (str):
                The BCP-47 language code for ``label``, such as "en-US" or
                "sr-Latn". For more information, see
                http://www.unicode.org/reports/tr35/#Unicode_locale_identifier.
        """
        label = proto.Field(proto.STRING, number=1)
        language_code = proto.Field(proto.STRING, number=2)

    web_entities = proto.RepeatedField(proto.MESSAGE, number=1, message=WebEntity)
    full_matching_images = proto.RepeatedField(
        proto.MESSAGE, number=2, message=WebImage
    )
    partial_matching_images = proto.RepeatedField(
        proto.MESSAGE, number=3, message=WebImage
    )
    pages_with_matching_images = proto.RepeatedField(
        proto.MESSAGE, number=4, message=WebPage
    )
    visually_similar_images = proto.RepeatedField(
        proto.MESSAGE, number=6, message=WebImage
    )
    best_guess_labels = proto.RepeatedField(proto.MESSAGE, number=8, message=WebLabel)


__all__ = tuple(sorted(__protobuf__.manifest))
