<span class="pager-links">
    % if pager.has_prev:
    ## Translators, used in the pager
    <a href="${i18n_path(request.path) + h.set_qparam(p=pager.page - 1).to_qs()}" class="button prev">${_('previous')}</a>
    % endif

    ${h.form(method='GET', _class='inline')}
        % if pager.pages > 1:
        <label for="page">${_('page')}</label>
        ${h.vselect('p', pager.page_choices, vals, _id='page')}
        % endif
        ${h.vselect('pp', pager.per_page_choices, vals, id='per-page')}
        <label for="per-page">${_('per page')}</label>
        <button type="submit">${_('Reload')}</button>
    </form>

    % if pager.has_next:
    ## Translators, used in the pager
    <a href="${i18n_path(request.path) + h.set_qparam(p=pager.page + 1).to_qs()}" class="button next">${_('next')}</a>
    % endif
</span>
