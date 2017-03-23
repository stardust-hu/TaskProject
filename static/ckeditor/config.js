/**
 * @license Copyright (c) 2003-2017, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.md or http://ckeditor.com/license
 */

CKEDITOR.editorConfig = function( config ) {
    config.language = 'zh-cn';
    config.height = 600;
    config.extraPlugins = 'uploadimage,codesnippet,mathjax';
    config.filebrowserUploadUrl="/imageUpload/";
    // config.uploadUrl    = '/upload_image';
    // config.mathJaxLib = '//cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML';
    config.mathJaxLib = '/static/js/MathJax/MathJax.js?config=TeX-AMS-MML_HTMLorMML';
    // config.image_previewText = '';
    // config.removeDialogTabs = 'image:info;image:Link;image:advanced';
    config.removeDialogTabs = 'image:Link;image:advanced';

    config.toolbarGroups = [
        { name: 'document', groups: [ 'document', 'mode', 'doctools' ] },
        { name: 'clipboard', groups: [ 'clipboard', 'undo' ] },
        { name: 'editing', groups: [ 'find', 'selection', 'spellchecker', 'editing' ] },
        { name: 'links', groups: [ 'links' ] },
        { name: 'insert', groups: [ 'insert' ] },
        { name: 'forms', groups: [ 'forms' ] },
        { name: 'tools', groups: [ 'tools' ] },
        { name: 'others', groups: [ 'others' ] },
        '/',
        { name: 'basicstyles', groups: [ 'basicstyles', 'cleanup' ] },
        { name: 'paragraph', groups: [ 'list', 'indent', 'blocks', 'align', 'bidi', 'paragraph' ] },
        { name: 'styles', groups: [ 'styles' ] },
        { name: 'colors', groups: [ 'colors' ] },
        { name: 'about', groups: [ 'about' ] }
    ];

    config.removeButtons = 'Underline,Subscript,Superscript,Source,Templates,About,Flash,Form,TextField,Textarea,Select,HiddenField,ImageButton,Button,CreateDiv,Language';

    config.codeSnippet_theme = 'tomorrow';
    config.codeSnippet_languages = {
        cpp: 'C++',
        matlab: 'MATLAB',
        python: 'Python',
        markdown: 'Markdown',
        xml: 'XML',
        java: 'JAVA',
        json: 'JSON',
        sql: 'SQL'
    };
};
