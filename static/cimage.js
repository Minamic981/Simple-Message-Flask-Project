const Inline = Quill.import('blots/block');

class CustomImage extends Inline {
    static create(value) {
        let node = super.create();
        node.setAttribute('src', value);
        node.setAttribute('alt', 'Image');
        node.setAttribute('style', 'max-width: 100%; height: auto;'); // Makes the image responsive
        return node;
    }

    static formats(node) {
        return node.getAttribute('src');
    }

    static formats(node) {
        return {
            src: node.getAttribute('src'),
            width: node.style.width,
            height: node.style.height,
        };
    }
}

CustomImage.blotName = 'custom-image';
CustomImage.tagName = 'img';

Quill.register(CustomImage);