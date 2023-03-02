function main(splash, args)
  splash:on_request(function(request)
    if request.url:find('css') then
      request.abort()
    end
    end)
  splash.images_enabled = false
  splash.js_enabled = false
  assert(splash:go(args.url))
  assert(splash:wait(0.5))
  return {
      html = splash:html()
  }
end